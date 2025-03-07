import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def prob(dE, *args):
    return np.exp(-dE/T)

def neighbours(i, j, *args):
    if i+1 > size-1:
        i_u = 0
    else:
        i_u = i+1
        
    if i-1 < 0:
        i_d = size-1
    else:
        i_d = i-1

    if j+1 > size-1:
        j_u = 0
    else:
        j_u = j+1
        
    if j-1 < 0:
        j_d = size-1
    else:
        j_d = j-1

    return i_u, i_d, j_u, j_d
    
def two_neighbours(i, j, *args):
    if i+1 > size-1:
        i_u = 0
    else:
        i_u = i+1
        
    if j+1 > size-1:
        j_u = 0
    else:
        j_u = j+1
        
    return i_u, j_u, 
    
def E_diff_glaub(i, j, i_u, i_d, j_u, j_d):
    E = -1 * (grid[i, j] * (grid[i_u, j] + grid[i_d, j] + grid[i, j_u] + grid[i, j_d]))

    E_2 = -1 * ((-1*grid[i, j]) * (grid[i_u, j] + grid[i_d, j] + grid[i, j_u] + grid[i, j_d]))
        
    return E_2 - E  
    
def E_diff_kawa(i_1, j_1, i_1_u, i_1_d, j_1_u, j_1_d,
                i_2, j_2, i_2_u, i_2_d, j_2_u, j_2_d):
    
    E_1 = -1 * (grid[i_1, j_1] * (grid[i_1_u, j_1] + grid[i_1_d, j_1] + grid[i_1, j_1_u] + grid[i_1, j_1_d]))
    
    E_2 = -1 * (grid[i_2, j_2] * (grid[i_2_u, j_2] + grid[i_2_d, j_2] + grid[i_2, j_2_u] + grid[i_2, j_2_d]))
    
    E_before = E_1 + E_2
    
    E_1 = -1 * (grid[i_2, j_2] * (grid[i_1_u, j_1] + grid[i_1_d, j_1] + grid[i_1, j_1_u] + grid[i_1, j_1_d]))
    
    E_2 = -1 * (grid[i_1, j_1] * (grid[i_2_u, j_2] + grid[i_2_d, j_2] + grid[i_2, j_2_u] + grid[i_2, j_2_d]))
    
    E_after = E_1 + E_2
    
    E_diff = E_after - E_before
    
    if [i_1, j_1]==[i_2_u, j_2] or [i_1, j_1]==[i_2_d, j_2] or [i_1, j_1]==[i_2, j_2_u] or [i_1, j_1]==[i_2, j_2_d]:
        E_diff += grid[i_1, j_1] * grid[i_2, j_2]
        
    return E_diff

def mag(grid):
    return np.sum(grid)

def glauber(*args):
    i = np.random.randint(0, size)
    j = np.random.randint(0, size)

    i_u, i_d, j_u, j_d = neighbours(i, j)
        
    dE = E_diff_glaub(i, j, i_u, i_d, j_u, j_d)
        
    if dE <= 0 or np.random.rand(1) <= prob(dE):
        grid[i,j] *= -1
           
    return grid
    
def kawasaki(*args):
    i_1 = np.random.randint(0, size)
    j_1 = np.random.randint(0, size)
    i_2 = np.random.randint(0, size)
    j_2 = np.random.randint(0, size)
    
    if grid[i_1, j_1] != grid[i_2, j_2]:

        i_1_u, i_1_d, j_1_u, j_1_d = neighbours(i_1, j_1)
        i_2_u, i_2_d, j_2_u, j_2_d = neighbours(i_2, j_2)
        
        dE = E_diff_kawa(i_1, j_1, i_1_u, i_1_d, j_1_u, j_1_d,
                         i_2, j_2, i_2_u, i_2_d, j_2_u, j_2_d)
                     
        if dE <= 0 or np.random.rand(1) <= prob(dE):
            grid[i_1, j_1], grid[i_2, j_2] = grid[i_2, j_2], grid[i_1, j_1]
        
    return grid
            
def total_energy(*args):
    E = 0
    for i in range(size):
        for j in range(size):
            i_u, j_u = two_neighbours(i, j)
            
            E += (-1 * (grid[i, j]*grid[i_u, j] + grid[i, j]*grid[i, j_u]))
        
    return E


def jackknife(data):

    n = len(data)
    mean_values = np.array([np.mean(np.delete(data, i)) for i in range(n)])
    mean_full = np.mean(data)
    variance = np.mean((mean_values - mean_full) ** 2)
    return np.sqrt(variance)

    


if __name__ == "__main__":

    size = int(sys.argv[1])
    nstep = 10000
    flag = False    
    
    #randomize spins in grid
    """
    for i in range(size):
        for j in range(size):
            if np.random.randint(2, size=1) == 1:
                grid[i,j] *= -1 """
    
    temp = np.arange(1, 3.1, 0.1)
    mag_avg_ls = []
    susc_ls = []
    E_avg_ls = []
    heat_cap_ls = []
    c_err_ls = []

    
    grid = -1 * np.ones([size, size])
    func = glauber
    
    for T in temp:
        print(T)
        mags = np.array([])
        energies = np.array([])
        
        
        for n in range(nstep):
            for i in range (size**2):
                grid = func()
                
            if n == 100:
                flag = True
            
            if n % 10 == 0:    
                #plt.cla()
                #im = plt.imshow(grid, animated = True)
                #plt.draw()
                #plt.pause(0.0001)
                #print(n)
                
                if flag == True:
                    mags = np.append(mags, mag(grid))    
                    energies = np.append(energies, total_energy(grid))
        
        mag_avg_ls.append(np.mean(mags))
        susc_ls.append(1/(T * size**2) * (np.mean(mags**2) - mag_avg_ls[-1]**2))
        
        E_avg_ls.append(np.mean(energies))
        heat_cap_ls.append(1/(T**2 * size**2) * (np.mean(energies**2) - E_avg_ls[-1]**2))
        
        c_err_ls.append(jackknife(energies))

    
        
    np.save("mag", mag_avg_ls)
    np.save("susc", susc_ls)
    np.save("energy", E_avg_ls)
    np.save("heat_cap", heat_cap_ls)
    np.save("temp", temp)
    np.save("c_err", c_err_ls)


        
        






