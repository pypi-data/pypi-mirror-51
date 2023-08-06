# Waiting for https://github.com/nielstron/quantulum3/issues/131 to be resolved
from quantulum3 import parser as UnitParser
from pint import UnitRegistry

units = UnitRegistry()

def parseToMicrometer(text):
    text = text.replace('Â', '')
    try:
        quantities = UnitParser.parse(text)
        if len(quantities) == 0:
            raise Exception("No quantity found where micrometers were expected")
        result = quantities[0]
        if result.unit.name == 'dimensionless':
            result.unit.name = 'micrometer'
        pq = units.Quantity(result.value, result.unit.name)
        return pq.to(units.micrometer).magnitude
    except Exception as e:
        raise Exception("Unable to parse '{}' to micrometer.".format(text))

def parseToDensity(text):
    text = text.replace('Â', '')
    try:
        quantities = UnitParser.parse(text)
        if len(quantities) == 0:
            raise Exception("No quantity found where a density was expected in '{}".format(text))
        result = quantities[0]
        if result.unit.name.find('cubic') == -1:
            raise Exception("A cubic unit is expected as density in '{}'".format(text))
        unitName = list(filter(lambda x: x != 'cubic' and x != 'per', result.unit.name.split(' ')))[-1]
        unit = units.Unit(unitName)
        pq = result.value * unit ** -3
        return pq.to(units.micrometer ** -3).magnitude
    except Exception as e:
        raise Exception("Unable to parse '{}' to density.".format(text))

def parseToPlanarDensity(text):
    text = text.replace('Â', '')
    try:
        quantities = UnitParser.parse(text)
        if len(quantities) == 0:
            raise Exception("No quantity found where a planar density was expected in '{}".format(text))
        result = quantities[0]
        if result.unit.name.find('square') == -1:
            raise Exception("A squared unit is expected as planar density in '{}'".format(text))
        unitName = list(filter(lambda x: x != 'squared' and x != 'square' and x != 'per', result.unit.name.split(' ')))[-1]
        unit = units.Unit(unitName)
        pq = result.value * unit ** -2
        return pq.to(units.micrometer ** -2).magnitude
    except Exception as e:
        raise Exception("Unable to parse '{}' to planar density.".format(text))

def parseToRadian(text):
    text = text.replace('Â', '')
    try:
        quantities = UnitParser.parse(text)
        if len(quantities) == 0:
            raise Exception("No quantity found where an angle was expected in '{}".format(text))
        result = quantities[0]
        unitName = result.unit.name.split(' ')[0]
        unit = units.Unit(unitName)
        pq = result.value * unit
        return pq.to(units.radian).magnitude
    except Exception as e:
        raise Exception("Unable to parse '{}' to radian angle.".format(text))
