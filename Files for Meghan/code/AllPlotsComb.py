import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np
from scipy.ndimage import gaussian_filter

RN = np.loadtxt("NRad.csv", delimiter=",")
RP = np.loadtxt("PRad.csv", delimiter=",")

binss = np.arange(0.05,20,0.1)
midss = []
for i in range(len(binss) - 1):
    m =(((binss[i] + binss[i + 1])/2 ))
    midss.append(m)


select = 40046

# Assuming pixel_array is your 2D or 3D array (for RGB images)
# For grayscale (2D array):
RadMax = RP.max()/select
    
plt.figure()                                                               
plt.plot(midss,RP/select,color = 'red')                                                              
plt.plot(midss,RN/(select*2),color = 'blue')
plt.xscale('log')
plt.xlim(0.1,20)
plt.ylim(0,RadMax*1.1 )
plt.title('Radius Mass Density')
plt.xlabel('Radius/$h^{-1}Mpc $')
plt.ylabel('Filament Mass density ($h^{-1}M_\odot$/$h^{-3}Mpc^3$)')
plt.savefig('PNradius.png')

plt.legend(['Physical','Non-physical'])

#MR
Nx_count = np.loadtxt("Nx_count_ds3.csv", delimiter=",")
Nx_count2 = np.loadtxt("Nx_count_ds4.csv", delimiter=",")

Px_count = np.loadtxt("Px_count_ds3.csv", delimiter=",")
Px_count2 = np.loadtxt("Px_count_ds4.csv", delimiter=",")

Nx_val = np.loadtxt("Nx_val_ds3.csv", delimiter=",")
Nx_val2 = np.loadtxt("Nx_val_ds4.csv", delimiter=",")

Px_val = np.loadtxt("Px_val_ds3.csv", delimiter=",")
Px_val2 = np.loadtxt("Px_val_ds4.csv", delimiter=",")

Nerrors_x = np.loadtxt("Nerrors_x_ds3.csv", delimiter=",")
Nerrors_x2 = np.loadtxt("Nerrors_x_ds4.csv", delimiter=",")

Perrors_x = np.loadtxt("Perrors_x_ds3.csv", delimiter=",")
Perrors_x2 = np.loadtxt("Perrors_x_ds4.csv", delimiter=",")

Nerrors_y = np.loadtxt("Nerrors_y_ds3.csv", delimiter=",")
Nerrors_y2 = np.loadtxt("Nerrors_y_ds4.csv", delimiter=",")

Perrors_y = np.loadtxt("Perrors_y_ds3.csv", delimiter=",")
Perrors_y2 = np.loadtxt("Perrors_y_ds4.csv", delimiter=",")

Pmidss_MR = np.loadtxt("Pmidss_ds3.csv", delimiter=",")
Nmidss_MR = np.loadtxt("Nmidss_ds3.csv", delimiter=",")
#errors_x2 = np.loadtxt("errors_x_MR (2).csv", delimiter=",")


MRlim1 = 2.75*10**13
MRlim2 = 3.7*10**13

MRlim3 = 4*10**14
MRlim4 = 5.2*10**14

plt.figure()
plt.errorbar(Nmidss_MR, Nx_val/Nx_count, xerr=Nerrors_x, yerr=Nerrors_y, fmt='-o',color = 'red', capsize=5, label='Data ± Error')  #gives errors if divide by 0
plt.errorbar(Pmidss_MR, Px_val/Px_count, xerr=Perrors_x, yerr=Perrors_y, fmt='-o',color = 'blue', capsize=5, label='Data ± Error')  #gives errors if divide by 0
plt.xlabel('Cluster separation/$h^{-1}Mpc $')
plt.ylabel('Total Filament Mass ($h^{-1}M_\odot$/$h^{-3}Mpc^3$)')
plt.xlim(0,1)
plt.ylim(MRlim3,MRlim4)
plt.legend(['Physical','Non-physical'])
plt.savefig('MR.png')

plt.figure()
plt.errorbar(Nmidss_MR, Nx_val2/Nx_count2, xerr=Nerrors_x2, yerr=Nerrors_y2,color = 'red', fmt='-o', capsize=5, label='Data ± Error')  #gives errors if divide by 0
plt.errorbar(Pmidss_MR, Px_val2/Px_count2, xerr=Perrors_x2, yerr=Perrors_y2, fmt='-o',color = 'blue', capsize=5, label='Data ± Error')  #gives errors if divide by 0
plt.xlabel('Cluster separation/$h^{-1}Mpc $')
plt.ylabel('Normalised Total Filament Mass ($h^{-1}M_\odot$/$h^{-3}Mpc^3 h^{-1}Mpc$)')
plt.xlim(0,1)
plt.ylim(MRlim1,MRlim2)
plt.legend(['Physical','Non-physical'])
plt.savefig('MRNorm.png')
#Sep
Nx_count = np.loadtxt("Nx_count_ds2.csv", delimiter=",")
Nx_count2 = np.loadtxt("Nx_count_ds2.csv", delimiter=",")

Px_count = np.loadtxt("Px_count_ds.csv", delimiter=",")
Px_count2 = np.loadtxt("Px_count_ds2.csv", delimiter=",")

Nx_val = np.loadtxt("Nx_val_ds2.csv", delimiter=",")
Nx_val2 = np.loadtxt("Nx_val_ds2.csv", delimiter=",")

Px_val = np.loadtxt("Px_val_ds.csv", delimiter=",")
Px_val2 = np.loadtxt("Px_val_ds2.csv", delimiter=",")

Nerrors_x = np.loadtxt("Nerrors_x_ds2.csv", delimiter=",")
Nerrors_x2 = np.loadtxt("Nerrors_x_ds2.csv", delimiter=",")

Perrors_x = np.loadtxt("Perrors_x_ds.csv", delimiter=",")
Perrors_x2 = np.loadtxt("Perrors_x_ds2.csv", delimiter=",")

Nerrors_y = np.loadtxt("Nerrors_y_ds2.csv", delimiter=",")
Nerrors_y2 = np.loadtxt("Nerrors_y_ds2.csv", delimiter=",")

Perrors_y = np.loadtxt("Perrors_y_ds.csv", delimiter=",")
Perrors_y2 = np.loadtxt("Perrors_y_ds2.csv", delimiter=",")

Pmidss_MR = np.loadtxt("Pmidss_ds2.csv", delimiter=",")
Nmidss_MR = np.loadtxt("Nmidss_ds2.csv", delimiter=",")
#errors_x2 = np.loadtxt("errors_x_MR (2).csv", delimiter=",")


MRlim1 = 2.35*10**13
MRlim2 = 3.3*10**13

MRlim3 = 0.8*10**14
MRlim4 = 6.5*10**14

plt.figure()
plt.errorbar(Pmidss_MR, Px_val/Px_count, xerr=Perrors_x, yerr=Perrors_y, fmt='-o',color='red', capsize=5, label='Data ± Error')  #gives errors if divide by 0
plt.errorbar(Nmidss_MR, (Nx_val/Nx_count)*Nmidss_MR, xerr=Nerrors_x, yerr=Nerrors_y, fmt='-o',color='blue', capsize=5, label='Data ± Error')  #gives errors if divide by 0
plt.xlabel('Cluster separation/$h^{-1}Mpc $')
plt.ylabel('Total Filament Mass ($h^{-1}M_\odot$/$h^{-3}Mpc^3$)')
plt.xlim(3,20)
plt.ylim(MRlim3,MRlim4)
plt.legend(['Physical','Non-physical'])
plt.savefig('Sep.png')

plt.figure()
plt.errorbar(Pmidss_MR, Px_val2/Px_count2, xerr=Perrors_x2, yerr=Perrors_y2, fmt='-o',color='red', capsize=5, label='Data ± Error')  #gives errors if divide by 0
plt.errorbar(Nmidss_MR, Nx_val2/Nx_count2, xerr=Nerrors_x2, yerr=Nerrors_y2, fmt='-o',color='blue',  capsize=5, label='Data ± Error')  #gives errors if divide by 0
plt.xlabel('Cluster separation/$h^{-1}Mpc $')
plt.ylabel('Normalised Total Filament Mass ($h^{-1}M_\odot$/$h^{-3}Mpc^3 h^{-1}Mpc$)')
plt.xlim(3,20)
plt.ylim(MRlim1,MRlim2)
plt.legend(['Physical','Non-physical'])
plt.savefig('SepNorm.png')

#Filament!
aP = np.loadtxt("PFilament.csv", delimiter=",")
aN = np.loadtxt("NFilament.csv", delimiter=",")
#aN = aN*2
comb = aP-aN

# Assuming pixel_array is your 2D or 3D array (for RGB images)
# For grayscale (2D array):
Psmoothed_array = gaussian_filter(aP, sigma=1.0)
Nsmoothed_array = gaussian_filter(aN, sigma=1.0)
PNsmoothed_array = gaussian_filter(comb, sigma=1.0)
PNNsmooth = Psmoothed_array-Nsmoothed_array
vmaxs = 148659184964
vmins = 17214854769
xedges = np.linspace(0, 100, 101)
X, Y = np.meshgrid((xedges[:-1] + xedges[1:]) / 2,
                   (xedges[:-1] + xedges[1:]) / 2)

#stacking
widths = 0.25

plt.figure()
plt.title('Non-Physical pairs Smoothed')
plt.imshow(Nsmoothed_array,norm=LogNorm(vmin = vmins,vmax = vmaxs))
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.axis('off')
plt.savefig('Non-Physical pairs Smoothed!.png')

plt.figure()
plt.title('Physical pairs Smoothed')
plt.imshow(Psmoothed_array,norm=LogNorm(vmin = vmins,vmax = vmaxs))
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.axis('off')
plt.savefig('Physical pairs Smoothed!.png')

plt.figure()
plt.title('Filament Smoothed')
plt.imshow(PNsmoothed_array,vmin = -0.5*10**10,vmax = 74334841610)
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.axis('off')
plt.savefig('Filament Smoothed! Non log.png')

plt.figure()
plt.title('Non-Physical pairs Smoothed')
plt.imshow(Nsmoothed_array,norm=LogNorm(vmin = vmins,vmax = vmaxs))
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.contour(X, Y, Nsmoothed_array,linewidths=widths, colors='black')
plt.axis('off')
plt.savefig('Non-Physical pairs Smoothed! contour.png')

plt.figure()
plt.title('Physical pairs Smoothed')
plt.imshow(Psmoothed_array,norm=LogNorm(vmin = vmins,vmax = vmaxs))
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.contour(X, Y, Psmoothed_array,linewidths=widths, colors='black')
plt.axis('off')
plt.savefig('Physical pairs Smoothed! contour.png')

plt.figure()
plt.title('Filament Smoothed')
plt.imshow(PNsmoothed_array,vmin = -0.5*10**10,vmax = 74334841610)
plt.plot(np.array([25,75]),np.array([50,50]),color = 'red',marker='*',markersize=12)  
plt.colorbar()
plt.contour(X, Y, PNsmoothed_array,linewidths=widths, colors='black')
plt.axis('off')
plt.savefig('Filament Smoothed!contour Non log.png')
