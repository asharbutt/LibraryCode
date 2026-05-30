import numpy as np
import matplotlib.pyplot as plt

def estimate_pi():
    n = 1000
    x = np.random.uniform(-1, 1, n)
    y = np.random.uniform(-1, 1, n)

    inside_circle = np.pow(x,2) + np.power(y,2) <= 1 # condition for being within a unit circle. pythagoras th

    total_inside = np.sum(inside_circle)

    pi_estimate = total_inside/n *4
    print(pi_estimate)

    cumulative_sum = np.cumsum(inside_circle)
    cumulative_sum_range = np.arange(1, n+1)
    rolling_estimate = cumulative_sum/cumulative_sum_range * 4


    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x[inside_circle], y[inside_circle], s=3, color="#2a9d8f", label="inside")
    ax.scatter(x[~inside_circle], y[~inside_circle], s=3, color="#e76f51", label="outside")

    # Reference circle and square
    theta = np.linspace(0, 2 * np.pi, 400)
    ax.plot(np.cos(theta), np.sin(theta), color="black", lw=1.5)
    ax.add_patch(plt.Rectangle((-1, -1), 2, 2, fill=False, color="black", lw=1.5))

    ax.set_aspect("equal")
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_title(f"Monte Carlo $\\pi \\approx$ {pi_estimate:.4f}  (n={n:,})")
    ax.axhline(y=0, color="black",ls="--", lw=1.5)
    ax.axvline(x=0, color="black", ls="--",lw=1.5)
    ax.legend(loc="upper right", markerscale=3)
    plt.tight_layout()
    plt.savefig("mc_pi.png", dpi=120)

    fig_2, ax_2 = plt.subplots(figsize=(6, 6))

    ax_2.plot(cumulative_sum_range, rolling_estimate, color="#2a9d8f", lw=1.5)
    ax_2.axhline(np.pi, color="black", ls="--", lw=1.5)
    ax_2.set_title("Monte Carlo Estimate Convergence to true $\\pi$")
    ax_2.set_ylabel("Estimated $\\pi$")
    ax_2.set_xlabel("n")

    plt.show()


estimate_pi()
