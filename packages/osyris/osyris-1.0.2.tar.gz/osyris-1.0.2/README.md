![demo.png](https://bitbucket.org/repo/jq5boX/images/2936418214-demo.png)

# Osyris #

A python visualization utility for RAMSES data.
Its purpose is to plot quick diagnostics while a simulation is running,
and also produce publication grade figures.

### Installation ###

```sh
pip install osyris
```

### From within ipython ###

```python
import osyris
mydata = osyris.RamsesData(71,scale="au")
osyris.plot_slice(mydata.log_rho,direction="z",vec=mydata.velocity,dx=100)
```

### Demo ###

You can download the sample data [here](http://www.nbi.dk/~nvaytet/osyris/ramses_sample_data.tar.gz).

```python
import osyris

# Load data
mydata = osyris.RamsesData(nout=71,center="max:density",scale="au")

# Create figure
fig = osyris.plt.figure()
ratio = 0.5
sizex = 20.0
fig.set_size_inches(sizex,ratio*sizex)
ax1 = fig.add_subplot(231)
ax2 = fig.add_subplot(232)
ax3 = fig.add_subplot(233)
ax4 = fig.add_subplot(234)
ax5 = fig.add_subplot(235)
ax6 = fig.add_subplot(236)

# Density vs B field with AMR level contours
osyris.plot_histogram(mydata.log_rho, mydata.log_B, axes=ax1, scalar=True,
                      scalar_args={"cmap": "log,YlGnBu"},
                      contour=mydata.level,
                      contour_args={"fmt": "%i", "label": True, "colors": "k",
                                    "cmap": None, "levels": range(5,20),
                                    "cbar": False})

# Create new field with log of velocity
mydata.new_field(name="log_vel",
                 operation="np.log10(np.sqrt(velocity_x**2+velocity_y**2+velocity_z**2))",
                 unit="cm/s",
                 label="log(Velocity)")

# Density vs log_vel in scatter mode with a grey outline
osyris.plot_histogram(mydata.log_rho ,mydata.log_vel, axes=ax2,
                      scatter=mydata.log_T,
                      scatter_args={"iskip": 100, "cmap": "gnuplot"},
                      outline=True)

#x,z density slice with B field streamlines
osyris.plot_slice(mydata.density, direction="y", stream=mydata.B, dx=100,
                  axes=ax3, scalar_args={"cmap": "log"})
# x,y density slice with velocity vectors in color
osyris.plot_slice(scalar=mydata.log_rho, direction="z", vec=mydata.velocity,
                  dx=100, axes=ax4, vec_args={"cmap": "seismic", "vskip": 4})
# x,y temperature slice with velocity vectors
osyris.plot_slice(mydata.log_T, direction="z", vec=mydata.velocity, dx=100,
                  axes=ax5, scalar_args={"cmap": "hot"}, contour=mydata.level,
                  contour_args={"fmt": "%i", "label": True, "colors": "w",
                                "cmap": None, "levels": range(9,17)})

# Now update values with later snapshot
mydata.update_values(201)
# Re-plot x,y density slice with velocity vectors
osyris.plot_slice(mydata.log_rho, direction="z", vec=mydata.velocity,
                  dx=100, axes=ax6)

fig.savefig("demo.pdf", bbox_inches="tight")
```

### Documentation ###

The documentation for `osyris` is hosted on [Readthedocs](https://osyris.readthedocs.io/en/latest/index.html).

### Have a problem or need a new feature? ###

Submit an issue on [Github](https://github.com/nvaytet/osyris/issues).

### Contributors ###

* Neil Vaytet (StarPlan/NBI)
* Tommaso Grassi (StarPlan/NBI)
* Matthias Gonzalez (CEA Saclay)
* Troels Haugbolle (StarPlan/NBI)
* Lucas Beeres

### Logo credit ###

[Icon vector created by frimufilms - www.freepik.com](https://www.freepik.com/free-photos-vectors/icon)