import random
import math
#--- COST FUNCTION ------------------------------------------------------------+
# Function to calculate Ct based on the provided formula
def cost_function(x):
Cbat, SOC, DOD, Qfade, u, Nb, Q = x
m, n, d = (1.2, 0.9, 0.1) # Curve fitting constants (replace with your actual values)
Pb = 0.8 # Constant (replace with your actual value)
Csoc = Cbat * (m * SOC - d) / (Qfade * n * Nb)
Cdod = Cbat / (Q * n * Nb * DOD * (u**2))
return Pb * max(Csoc, Cdod)
#--- PARTICLE CLASS -----------------------------------------------------------+
class Particle:
def __init__(self, x0):
self.position_i = [] # Particle position (variables)
self.velocity_i = [] # Particle velocity
self.pos_best_i = [] # Best position found by the particle
self.err_best_i = float("inf") # Best cost (Ct) found by the particle
self.err_i = float("inf") # Current cost (Ct) of the particle
for i in range(len(x0)):
self.velocity_i.append(random.uniform(-1, 1))
self.position_i.append(x0[i])
# Evaluate current fitness (cost)
def evaluate(self):
self.err_i = cost_function(self.position_i)
# Check if current position is the particle's best
if self.err_i < self.err_best_i:
self.pos_best_i = self.position_i.copy()
self.err_best_i = self.err_i
# Update particle velocity
def update_velocity(self, pos_best_g):
w = 0.3 # Inertia weight
c1 = 2 # Cognitive constant
c2 = 1.5 # Social constant
for i in range(len(self.position_i)):
r1 = random.random()
r2 = random.random()
cognitive_velocity = c1 * r1 * (self.pos_best_i[i] - self.position_i[i])
social_velocity = c2 * r2 * (pos_best_g[i] - self.position_i[i])
self.velocity_i[i] = w * self.velocity_i[i] + cognitive_velocity + social_velocity
# Update particle position based on new velocity
def update_position(self, bounds):
for i in range(len(self.position_i)):
self.position_i[i] = self.position_i[i] + self.velocity_i[i]
# Adjust position if it exceeds bounds
if self.position_i[i] > bounds[i][1]:
self.position_i[i] = bounds[i][1]
elif self.position_i[i] < bounds[i][0]:
self.position_i[i] = bounds[i][0]
#--- PSO CLASS ----------------------------------------------------------------+
class PSO:
def __init__(self, cost_func, x0, bounds, num_particles, maxiter):
global num_dimensions
num_dimensions = len(x0)
err_best_g = float("inf") # Best cost (Ct) found so far
pos_best_g = [] # Best position (variables) found so far
# Initialize the swarm
swarm = []
for i in range(num_particles):
swarm.append(Particle(x0))
cost_history = []
# Optimization loop
for i in range(maxiter):
# Evaluate fitness of each particle
for j in range(num_particles):
swarm[j].evaluate()
cost_history.append(swarm[j].err_i)
# Update global best if necessary
if swarm[j].err_i < err_best_g:
pos_best_g = swarm[j].position_i.copy()
err_best_g = swarm[j].err_i
# Update velocity and position of each particle
for j in range(num_particles):
swarm[j].update_velocity(pos_best_g)
swarm[j].update_position(bounds)
# Print final results
print("FINAL:")
print(f"Best Cost (Ct): {err_best_g:.4f}")
print(f"Best Variables: {pos_best_g}")
import matplotlib.pyplot as plt
plt.plot(range(maxiter * num_particles), cost_history)
plt.xlabel("Iteration")
plt.ylabel("Cost Function (Ct)")
plt.title("Cost Function vs Max Iterations")
plt.show()
#--- MAIN SCRIPT ---------------------------------------------------------------+
if __name__ == "__main__":
# Initial starting position (replace with your initial guess for variables)
initial_guess = [10, 0.5, 0.2, 1.2, 2, 3, 5]
# Define variable bounds (replace with appropriate ranges for your variables)
bounds = [
(5, 15), # Cbat
(0.2, 0.8), # SOC
(0.1, 0.3), # DOD
(0.8, 1.5), # Qfade
(1, 3), # u
(1, 5), # Nb
(2, 8), # Q
]
# PSO parameters
num_particles = 20 # Number of particles in the swarm
max_iterations = 12 # Maximum iterations
# Run PSO optimization
pso = PSO(cost_function, initial_guess, bounds, num_particles, max_iterations)
