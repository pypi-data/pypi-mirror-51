import logging
from typing import List

from assemblyline.common import forge
from assemblyline.common import log as al_log
from assemblyline.common.classification import InvalidClassification
from assemblyline.common.dict_utils import unflatten
from assemblyline.common.str_utils import StringTable, safe_str
from assemblyline.odm.models.heuristic import Heuristic
from assemblyline.odm.models.result import ResultBody, Section, Heuristic
from assemblyline.odm.models.tagging import Tagging
from assemblyline_v4_service.common.helper import get_heuristics, get_service_attributes

al_log.init_logging('service.result')
log = logging.getLogger('assemblyline.service.result')

Classification = forge.get_classification()
SERVICE_ATTRIBUTES = get_service_attributes()

BODY_FORMAT = StringTable('BODY_FORMAT', [
    ('TEXT', 0),
    ('MEMORY_DUMP', 1),
    ('GRAPH_DATA', 2),
    ('URL', 3),
    ('JSON', 4)
])


class ResultSection:
    def __init__(
            self,
            title_text: str or list,
            body: str = None,
            classification: Classification = SERVICE_ATTRIBUTES.default_result_classification,
            body_format: BODY_FORMAT = BODY_FORMAT.TEXT,
            heuristic: Heuristic = None,
            tags: Tagging = None,
            parent=None,
    ):
        self._finalized: bool = False
        self._parent = parent
        self._section = None
        self.subsections: List[ResultSection] = []
        self.body: str = body
        self.classification: Classification = classification
        self.body_format: BODY_FORMAT = body_format
        self.depth: int = 0
        self.heuristic: Heuristic or None = heuristic
        self.tags = tags or {}

        if isinstance(title_text, list):
            title_text = ''.join(title_text)
        self.title_text = safe_str(title_text)

        if parent is not None:
            parent.add_section(self)

    def add_line(self, text: str or list) -> None:
        # add_line with a list should join without newline seperator.
        # use add_lines if list should be split one element per line.
        if isinstance(text, list):
            text = ''.join(text)
        textstr = safe_str(text)
        if self.body:
            textstr = '\n' + textstr
            self.body = self.body + textstr
        else:
            self.body = textstr

    def add_lines(self, line_list: list) -> None:
        if not isinstance(line_list, list):
            log.warning(f"add_lines called with invalid type: {type(line_list)}. ignoring")
            return

        segment = '\n'.join(line_list)
        if self.body is None:
            self.body = segment
        else:
            self.body = self.body + '\n' + segment

    def add_subsection(self, subsection, on_top: bool = False) -> None:
        """
        Add a result subsection to another result section or subsection.

        :param subsection: Subsection to add to another result section or subsection
        :param on_top: Display this result section on top of other subsections
        """
        if on_top:
            self.subsections.insert(0, subsection)
        else:
            self.subsections.append(subsection)
        subsection.parent = self

    def add_tag(self, tag_type: str, value: str) -> None:
        if tag_type not in self.tags:
            self.tags[tag_type] = []

        if value not in self.tags[tag_type]:
            self.tags[tag_type].append(value)

    def finalize(self, depth: int = 0) -> bool:
        if self._finalized:
            raise Exception("Double finalize() on result detected.")
        self._finalized = True

        keep_me = True
        tmp_subs = []
        self.depth = depth
        for subsection in self.subsections:
            subsection.finalize(depth=depth+1)
            # Unwrap it if we're going to keep it
            if subsection in self.subsections:
                tmp_subs.append(subsection)
        self.subsections = tmp_subs

        # At this point, all subsections are finalized and we're not deleting ourself
        if self._parent is not None:
            try:
                self._parent.classification = \
                    Classification.max_classification(self.classification, self._parent.classification)
            except InvalidClassification as e:
                log.error(f"Failed to finalize section due to a classification error: {str(e)}")
                keep_me = False

        return keep_me

    def set_body(self, body: str, body_format: BODY_FORMAT = BODY_FORMAT.TEXT) -> None:
        self.body = body
        self.body_format = body_format

    def set_heuristic(self, heur_id: str, attack_id: str = None) -> None:
        """
        Set a Heuristic for a result section/subsection. A Heuristic is required to assign a score to a result section/subsection.

        :param heur_id: Heuristic ID as set in the service manifest
        :param attack_id: (optional)
        """
        if self.heuristic:
            log.warning(f"A Heuristic ({self.heuristic.heur_id}) already exists for this section. "
                        f"Setting a new Heuristic ({heur_id}) will replace the existing Heuristic.")

        heuristics = get_heuristics()
        for heuristic in heuristics:
            if heur_id == heuristic.heur_id:
                self.heuristic = Heuristic(dict(
                    heur_id=heur_id,
                    attack_id=attack_id or heuristic.attack_id,
                    score=heuristic.score,
                ))

        if not self.heuristic:
            log.warning(f"Invalid Heuristic. A Heuristic must be added to the service manifest before using it.")


class Result:
    def __init__(self, sections: List[ResultSection] = None) -> None:
        self._flattened_sections: List[Section] = []
        self._score: int = 0
        self.sections: List[ResultSection] = sections or []

    def _append_section(self, section: ResultSection) -> None:
        self._flattened_sections.append(Section(dict(
            body=section.body,
            classification=section.classification,
            body_format=section.body_format,
            depth=section.depth,
            heuristic=section.heuristic,
            tags=unflatten(section.tags),
            title_text=section.title_text,
        )))

    def _flatten_sections(self, section: ResultSection, root: bool = True) -> None:
        if len(section.subsections) > 0:
            if root:
                self._append_section(section)

            for subsection in section.subsections:
                self._append_section(subsection)
                if len(subsection.subsections) > 0:
                    self._flatten_sections(subsection, root=False)
        else:
            self._append_section(section)

    def add_section(self, section: ResultSection, on_top: bool = False) -> None:
        """
        Add a result section to the root of the result.

        :param section: Section to add to the root of the result
        :param on_top: Display this result section on top of other sections
        """
        if on_top:
            self.sections.insert(0, section)
        else:
            self.sections.append(section)

    def finalize(self) -> ResultBody:
        to_delete_sections = []

        for section in self.sections:
            section.parent = self
            if not section.finalize():
                to_delete_sections.append(section)

        # Delete sections we can't keep
        for section in to_delete_sections:
            self.sections.remove(section)

        # Flatten all the sections into a flat list
        for section in self.sections:
            self._flatten_sections(section)

        # Calculate the total score of all sections/subsections
        for section in self._flattened_sections:
            if section.heuristic:
                self._score += section.heuristic.score

        result = ResultBody(dict(
            score=self._score,
            sections=self._flattened_sections,
        ))

        return result
