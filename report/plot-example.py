import matplotlib.pyplot as plt
from pathlib import Path

plot_folder = Path("./")

fig = plt.figure()
xpoints = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
ypoints_a = [1.0, 0.6, 1.3, 3.4, 3.4, 5.3, 7.4, 13.3, 9.5, 15.6]
ypoints_b = [5.3, 6.6, 8.3, 6.4, 7.4, 5.9, 8.4, 9.3, 10.5, 8.6]
plt.ylabel('Some metric')
plt.xlabel('Something that varies')
plt.plot(xpoints, ypoints_a, color='#ff9933', marker='o', linestyle='dashed', label="Method a")
plt.plot(xpoints, ypoints_b, color='#009999', marker='o', linestyle='dotted', label="Method b")
plt.legend(loc='upper left')
filename = plot_folder / "figure_example" ".pdf"
# uncomment the following to show the plot before saving it
# plt.show()
plt.savefig(filename)
plt.close(fig)
