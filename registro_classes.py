from nave import Nave
from asteroide import Asteroide
from projetil import Projetil
from ovni import OVNI
from ovni_x import OvniX
from ovni_cruz import OvniCruz
from ovni_projetil import OVNIProjetil

CLASSE_MAP = {
    'Nave': Nave,
    'Projetil': Projetil,
    'Asteroide': Asteroide,
    'OVNI': OVNI,
    'OVNIProjetil': OVNIProjetil,
    'OvniX': OvniX,
    'OvniCruz': OvniCruz,
}
