import xml.etree.ElementTree as ET
from typing import Dict, Any


class ErknmParser:
    """Парсер XML данных проверок ERKNM"""

    def __init__(self, xml_data: str):
        """
        Инициализация парсера
        :param xml_data: Путь к файлу XML с данными проверки ЕРКНМ
        """
        self.root = ET.parse(xml_data).getroot()
        self.ns = {'tns': self.root.tag.split('}')[0].split('{')[1]}


    def parse(self) -> Dict[str, Any]:
        """Основной метод парсинга XML данных"""
        return {
            'knm_date': self._parse_date(),
            'decision': self._parse_decision(),
            'inspectors': self._parse_inspectors(),
            'kind_control': self._parse_kind_control(),
            'kind_knm': self._parse_kind_knm(),
            'kno_organization': self._parse_kno_organization(),
            'objects_data': self._parse_objects(),
            'places': self._parse_places(),
            'reason_risk': self._parse_reason_risk(),
            'subject': self._parse_organizations(),
        }

    def _parse_date(self) -> Dict:
        knm_date = self.root.attrib
        return knm_date


    def _parse_kind_control(self) -> Dict:
        element = self.root.find('tns:KIND_CONTROL', self.ns)
        return element.attrib if element is not None else {}

    def _parse_kind_knm(self) -> Dict:
        element = self.root.find('tns:KIND_KNM', self.ns)
        return element.attrib if element is not None else {}

    def _parse_organizations(self) -> Dict:
        org = self.root.find('tns:ORGANIZATIONS', self.ns)
        okved = org.find('tns:OKVEDS', self.ns)
        return {
            'organizations': org.attrib if org else {},
            'okveds': okved.attrib,
        }

    def _parse_objects(self) -> Dict:
        objects_node = self.root.find('tns:OBJECTS', self.ns)
        if not objects_node:
            return {}

        return {
            'object_type': self._find_attrib(objects_node, 'tns:OBJECT_TYPE'),
            'object_kind': self._find_attrib(objects_node, 'tns:OBJECT_KIND'),
            'object_sub_kind': self._find_attrib(objects_node, 'tns:OBJECT_SUB_KIND'),
            'risk_category': self._find_attrib(objects_node, 'tns:RISK_CATEGORY')
        }

    def _parse_inspectors(self) -> list:
        inspectors = []
        for element in self.root.findall('tns:INSPECTORS', self.ns):
            position = element.find('tns:INSPECTOR_POSITION', self.ns)
            inspectors.append({
                'full_name': element.get('INSPECTOR_FULL_NAME'),
                'guid': element.get('GUID'),
                'position': position.get('TITLE')
            })
        return inspectors

    def _parse_places(self) -> str:
        element = self.root.find('tns:PLACES', self.ns)
        return element.text if element is not None else ''

    def _parse_decision(self) -> Dict:
        element = self.root.find('tns:DECISION', self.ns)

        title = element.find('tns:TITLE_SIGNER', self.ns)
        return {
            'signer': element.get('FIO_SIGNER'),
            'title': title.get('TITLE')
        }

    def _parse_reason_risk(self) -> Dict:
        element = self.root.find('tns:REASON_RISK', self.ns)
        if not element:
            return {}

        reason = element.find('tns:REASON', self.ns)
        reason_type = reason.find('tns:REASON_TYPE', self.ns) if reason else None

        return {
            'main': reason.get('MAIN') if reason else None,
            'approve_required': reason.get('APPROVE_REQUIRED') if reason else None,
            'reason_type': reason_type.attrib
        }

    def _find_attrib(self, parent, path: str) -> Dict:
        element = parent.find(path, self.ns)
        return element.attrib if element is not None else {}

    def _parse_kno_organization(self):
        element = self.root.find('tns:KNO_ORGANIZATION', self.ns)
        return element.attrib if element is not None else {}