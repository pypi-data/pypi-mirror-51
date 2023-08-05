import time

from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.result import Result, ResultSection


class ExampleService(ServiceBase):
    def __init__(self, config=None):
        super(ExampleService, self).__init__(config)

    def start(self):
        self.log.info(f"start() from {self.service_name} service called")

    def execute(self, request):
        time.sleep(1)
        result = Result()

        section = ResultSection(title_text="Section with only tags", body="Example service completed")
        section.add_tag('attribution.actor', 'testValue')
        section.add_tag('network.ip', '192.168.0.1')
        section.add_line("Nothing done.")
        result.add_section(section)

        section = ResultSection("Section with Heuristic and Tags")
        section.set_heuristic('example_service_1')
        section.add_tag('av.virus_name', 'ImABadVirus')
        result.add_section(section)

        section = ResultSection("Section with subsections")
        subsection1 = ResultSection("Subsection #1")
        subsection2 = ResultSection("Subsection #2")
        subsection21 = ResultSection("Subsection #2.1")
        subsection21.add_tag('network.ip', '192.168.0.2')
        subsection2.add_subsection(subsection21)
        subsection21a = ResultSection("Subsection #2.1.a")
        subsection21a.add_lines(["This is line #1", "This is line #2", "This is line #3"])
        subsection21.add_subsection(subsection21a)
        section.add_subsection(subsection1)
        section.add_subsection(subsection2)
        result.add_section(section)

        request.result = result
