# Ще създам електрическа схема въз основа на предоставената информация.
# Използвам Python за чертане на електрическата схема.

import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    # PWM генератор (TL494)
    pwm = d.add(elm.RBox(w=2, h=1.5, label='TL494\nPWM'))

    # Транзистори BC547
    bc1 = d.add(elm.BjtNpn(label='BC547'))
    bc2 = d.add(elm.BjtNpn(label='BC547', at=(3, 0)))

    # Свързване на базите към PWM изход
    d.add(elm.Line().right().at(pwm.).length(0.5))
    d.add(elm.Resistor().down().label('1kΩ'))
    d.add(elm.Line().right().at((0.5, -1)).length(0.5).to(bc1.base))

    d.add(elm.Line().right().at((3, -1)).length(0.5).to(bc2.base))

    # Колекторите към MOSFET транзистори (IRF540N)
    mos1 = d.add(elm.Nmos(label='IRF540N', at=(0, -2.5)))
    mos2 = d.add(elm.Nmos(label='IRF540N', at=(3, -2.5)))

    d.add(elm.Resistor().down().at(bc1.collector).label('10Ω'))
    d.add(elm.Line().to(mos1.gate))

    d.add(elm.Resistor().down().at(bc2.collector).label('10Ω'))
    d.add(elm.Line().to(mos2.gate))

    # Дрените на MOSFET към захранване
    d.add(elm.Line().up().at(mos1.drain).length(1))
    d.add(elm.Vdd().label('12V-24V'))

    d.add(elm.Line().up().at(mos2.drain).length(1))
    d.add(elm.Vdd().label('12V-24V'))

    # Изход към LC филтър
    d.add(elm.Line().right().at(mos1.source).length(2))
    d.add(elm.Inductor().right().label('22µH – 100µH'))
    d.add(elm.Capacitor().down().label('1µF – 2.2µF'))
    d.add(elm.Ground())

    d.save('/amplifier.png')
