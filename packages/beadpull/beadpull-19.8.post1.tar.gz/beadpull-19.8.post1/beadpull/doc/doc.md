%Bead pull

# License

Copyright (C) 2019  S.V. Matsievskiy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Program source files may be found at <https://gitlab.com/matsievskiysv/beadpull>

# Equations

General equation:

$$
\frac{\Delta f}{f} = - \frac{V_1}{4 W}\left[
\frac{
\varepsilon_0 E_{0i}^2
}{
p_i + (\varepsilon-1)^{-1}
}
+
\frac{
\mu_0 H_{0i}^2
}{
m_i + (\mu-1)^{-1}
}
\right].
$$

Simplified equation:

$$
\frac{\Delta f}{f} =
\frac{
- \displaystyle\sum_{i=1}^{N}{k^E_i E_{0i}^2} +
\displaystyle\sum_{i=1}^{N}{k^H_i H_{0i}^2}
}{W},
$$

where
$$
k^E_i = \frac{V_1}{4}\frac{\varepsilon_0}
{(\varepsilon - 1 + p_i)}
$$
is an electric field form-factor,
$$
k^H_i = \frac{V_1}{4}\frac{\mu_0}{(\mu - 1 + m_i)}
$$
is a magnetic field form-factor.

## Direct $\Delta f$ measurements

Normalized electric field:

$$
\xi = \frac{E}{\sqrt{P Q}} =
\sqrt{\frac{\Delta f}{2 \pi k^E f_0^2}}
\left[\frac{\text{Ohm}^{1/2}}{\text{m}}\right].
$$

Normalized magnetic field:

$$
\varsigma = \frac{H}{\sqrt{P Q}} =
\sqrt{\frac{\Delta f}{2 \pi k^H f_0^2}}
\left[\frac{\text{???}}{\text{???}}\right].
$$

## Reflection $\Delta \dot S_{11}$ measurements

$$
\Delta \dot S_{11} = \dot S_{11} - \dot S_{11}^0 = \dot C \dot E^2,
$$

where $\dot S_{11}^0$ is a complex reflection in absence of bead.

Formula for normalized electric field:

$$
\hat E_n = \sqrt{\frac{|\dot S_{11}^n - \dot S_{11}^0|}
{2 \pi k^S f_0^2}}.
$$

Formula for electric field phase:

$$
\varphi_{n} = \frac{\varphi_{n} - \varphi_{0}}{2}.
$$

## Transmission $\Delta \varphi$ measurements

Using the following equation:
$$\Delta f = \frac{f_0}{2 Q_{load}} \tan{\Delta \varphi}
\approx \frac{f_0 \Delta \varphi}{2 Q_{load}}, |\Delta \varphi| \le 5^\circ$$

Normalized electric field:

$$
\xi = \frac{E}{\sqrt{P Q}} =
\sqrt{\frac{\Delta \varphi}{4 \pi k^E f_0 Q_{load}}}
\left[\frac{\text{Ohm}^{1/2}}{\text{m}}\right].
$$

Normalized magnetic field:

$$
\varsigma = \frac{H}{\sqrt{P Q}} =
\sqrt{\frac{\Delta \varphi}{4 \pi k^H f_0 Q_{load}}}
\left[\frac{\text{???}}{\text{???}}\right].
$$

# Frequency response

| Bead material | E-field | H-filed |
|:-:|:-:|:-:|
| Metallic bead | ↓ | ↑ |
| Dielectric bead  | ↓ | ↓ |

Dielectric bead with $\varepsilon > 1, \mu = 1$ only measures electric field;
with $\varepsilon = 1, \mu > 1$ only measures magnetic field.

**For $\varepsilon \gg 1$ or $\mu \gg 1$ some equation approximations do not hold!**

# References

1. [Bead-pulling Measurement Principle and Technique Used for the SRF Cavities at JLab, Haipeng Wang](https://www.jlab.org/indico/event/98/contribution/7/material/slides/1.pdf)
1. A.Yu. Smirnov PhD thesis
