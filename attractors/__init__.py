from .rossler import RosslerAttractor
from .lorenz import LorenzAttractor
from .halvorsen import HalvorsenAttractor
from .aizawa import AizawaAttractor
from .thomas import ThomasAttractor

def select_attractor(name, params):
    name = name.lower()
    preset = params.ATTRACTOR_PRESETS[name]

    # Extract dt and initial conditions
    dt = preset["dt"] * params.CHAOS_GEARING
    x, y, z = preset["init"]

    # Dispatch to the correct attractor class
    if name == "lorenz":
        return LorenzAttractor(x=x, y=y, z=z, dt=dt)

    elif name == "rossler":
        return RosslerAttractor(x=x, y=y, z=z, dt=dt)

    elif name == "halvorsen":
        return HalvorsenAttractor(x=x, y=y, z=z, dt=dt)

    elif name == "aizawa":
        return AizawaAttractor(x=x, y=y, z=z, dt=dt)

    elif name == "thomas":
        return ThomasAttractor(x=x, y=y, z=z, dt=dt)

    else:
        raise ValueError(f"Unknown attractor: {name}")
