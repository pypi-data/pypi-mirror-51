from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plonetheme.nuplone.z3cform.interfaces import INuPloneFormLayer


class IClientSkinLayer(IDefaultBrowserLayer, INuPloneFormLayer):
    """Zope skin layer for the online client.
    """


class IIdentificationPhaseSkinLayer(Interface):
    """Skin layer used during the identification phase."""


class ICustomizationPhaseSkinLayer(Interface):
    """Skin layer used during the custom risk phase."""


class IEvaluationPhaseSkinLayer(Interface):
    """Skin layer used during the evaluation phase."""


class IActionPlanPhaseSkinLayer(Interface):
    """Skin layer used during the action plan phase."""


class IReportPhaseSkinLayer(Interface):
    """Skin layer used during the report phase."""


# Special case for individual countries...

class IItaly(Interface):
    """Skin layer to mark the country Italy"""

class IItalyIdentificationPhaseSkinLayer(IItaly, IIdentificationPhaseSkinLayer):
    """Skin layer to mark the country Italy"""

class IItalyCustomizationPhaseSkinLayer(IItaly, ICustomizationPhaseSkinLayer):
    """Skin layer to mark the country Italy"""

class IItalyEvaluationPhaseSkinLayer(IItaly, IEvaluationPhaseSkinLayer):
    """Skin layer to mark the country Italy"""

class IItalyActionPlanPhaseSkinLayer(IItaly, IActionPlanPhaseSkinLayer):
    """Skin layer to mark the country Italy"""

class IItalyReportPhaseSkinLayer(IItaly, IReportPhaseSkinLayer):
    """Skin layer to mark the country Italy"""


class IFrance(Interface):
    """Skin layer to mark the country France"""

class IFranceIdentificationPhaseSkinLayer(IFrance, IIdentificationPhaseSkinLayer):
    """Skin layer to mark the country France"""

class IFranceCustomizationPhaseSkinLayer(IFrance, ICustomizationPhaseSkinLayer):
    """Skin layer to mark the country France"""

class IFranceEvaluationPhaseSkinLayer(IFrance, IEvaluationPhaseSkinLayer):
    """Skin layer to mark the country France"""

class IFranceActionPlanPhaseSkinLayer(IFrance, IActionPlanPhaseSkinLayer):
    """Skin layer to mark the country France"""

class IFranceReportPhaseSkinLayer(IFrance, IReportPhaseSkinLayer):
    """Skin layer to mark the country France"""
