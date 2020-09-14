import cartopy.crs as ccrs
import matplotlib
import numpy as np
import os
import time
import xarray as xr

from matplotlib import pyplot as plt
import matplotlib.animation as animation


# This script plots animations of the SIF netcdf4 files as a function of time

# Options for running the code:
baseline_file = "./data/tropomi/gridded/TROPO_SIF_03-2018.nc"
all_files = [
    "./data/tropomi/gridded/" + file for file in os.listdir("./data/tropomi/gridded/")
]
savename = "output/initial_plot_light.gif"
t0 = 7  # The initial data is all blank
tend = 100  # Demonstrates importing data across files

# Load data
all_data = xr.open_mfdataset(all_files)
fig, ax = plt.subplots()

# Define functions for plotting
# For some reason the database contains very extreme values. Most lie in a smaller range
min_data = -3  # all_data.SIF.min(skipna=True).values
max_data = 5  # all_data.SIF.max(skipna=True).values

def date_conv(day):
    return day.astype('datetime64[D]')

title_str = "Date: {}"
fig = plt.figure(figsize=(8, 4))
ax = plt.axes(projection=ccrs.PlateCarree())
cmap = matplotlib.cm.get_cmap("viridis")  # "gist_earth"
cmap.set_bad("white", 1.0)
plot_options = {
   "vmax": max_data,
   "vmin": min_data,
    "cmap": cmap,
}


def animate(i):
    line = ax.imshow(
        all_data.SIF[i, :, :], **plot_options
    )
    date = date_conv(all_data.time[i].values)
    plt.title(title_str.format(date))
    return line


def init():
    line = animate(t0)
    cb = plt.colorbar(line, ax=ax, format="%g")
    cb.ax.set_ylabel("SIF")


writer = animation.writers["pillow"]
writer = writer(fps=4, metadata=dict(artist="Robin Lamboll"), bitrate=-1)

# Call the animator.  blit=True would mean only re-draw the parts that have changed.
anim = animation.FuncAnimation(
    plt.gcf(), animate, frames=np.arange(t0, tend), init_func=init, interval=200,
    blit=False
)
# Save the animation
timestart = time.time()
anim.save(savename, writer=writer)
print("Animation took {}".format(time.time() - timestart))
