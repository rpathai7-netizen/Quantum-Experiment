import os
import time

import numpy as np
import psutil
import quimb.tensor as qtn


def get_ram_usage_gb():
    """Returns the current Resident Set Size (RSS) memory of the process in GB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024**3)


def create_nuclear_pasta_3d(L, chi):
    """
    Constructs a 3D Projected Entangled Pair State (PEPS) on an LxLxL lattice.
    Each node represents a 'pasta' cluster in a neutron star crust.
    """
    tn = qtn.TensorNetwork([])

    # We use a 3D grid of indices
    # Each site (i, j, k) has up to 6 virtual bonds and 1 physical bond.
    for i in range(L):
        for j in range(L):
            for k in range(L):
                # Bond names for current site
                # x-dim: index shared with (i+1, j, k)
                # y-dim: index shared with (i, j+1, k)
                # z-dim: index shared with (i, j, k+1)

                inds = []
                # Virtual bonds (shared with neighbors)
                # X-axis
                if i > 0:
                    inds.append(f"x_{i-1}_{j}_{k}")
                if i < L - 1:
                    inds.append(f"x_{i}_{j}_{k}")
                # Y-axis
                if j > 0:
                    inds.append(f"y_{i}_{j-1}_{k}")
                if j < L - 1:
                    inds.append(f"y_{i}_{j}_{k}")
                # Z-axis
                if k > 0:
                    inds.append(f"z_{i}_{j}_{k-1}")
                if k < L - 1:
                    inds.append(f"z_{i}_{j}_{k}")

                # Physical index (representing the local state of the crust)
                inds.append(f"phys_{i}_{j}_{k}")

                # Create a random tensor for this site
                # Shape: (chi, chi, ..., 2)
                # Number of chi-dims is the number of virtual neighbors
                shape = tuple([chi] * (len(inds) - 1)) + (2,)
                data = np.random.randn(*shape).astype(
                    np.float32
                )  # float32 to save a bit of RAM

                t = qtn.Tensor(
                    data=data, inds=inds, tags={f"SITE_{i}_{j}_{k}", "PASTA_CRUST"}
                )
                tn.add_tensor(t)

    return tn


def run_simulation():
    L = 3  # 3x3x3 Cube
    RAM_LIMIT_GB = 80.0

    print("=" * 60)
    print("      NUCLEAR PASTA 3D - NEUTRON STAR CRUST SIMULATOR")
    print("=" * 60)
    print(f"Lattice Geometry: {L}x{L}x{L} ({L**3} nodes)")
    print(f"Safety Threshold: {RAM_LIMIT_GB} GB RAM")
    print("-" * 60)

    max_chi = 1
    try:
        for chi in range(1, 100):  # Theoretical upper bound
            current_ram = get_ram_usage_gb()
            if current_ram > RAM_LIMIT_GB:
                print(
                    f"\n[!!!] CRITICAL: RAM Limit Reached ({current_ram:.2f} GB > {RAM_LIMIT_GB} GB)"
                )
                break

            print(
                f"Bond Dimension chi = {chi:2d} | Current RAM: {current_ram:>7.4f} GB ... ",
                end="",
                flush=True,
            )

            # 1. Generate the network
            tn = create_nuclear_pasta_3d(L, chi)

            # 2. Contract the network
            # To simulate a physical observable, we contract to a scalar
            # (e.g., by tracing out physical indices)
            for i in range(L):
                for j in range(L):
                    for k in range(L):
                        tn.contract_ind(f"phys_{i}_{j}_{k}")

            start_time = time.time()
            # Perform optimized contraction
            # quimb uses cotengra or greedy paths to minimize intermediate tensors
            result = tn.contract(optimize="greedy")
            duration = time.time() - start_time

            final_ram = get_ram_usage_gb()
            print(
                f"Done ({duration:6.3f}s) | Post-Contraction RAM: {final_ram:>7.4f} GB"
            )
            max_chi = chi

            if final_ram > RAM_LIMIT_GB:
                print(
                    f"\n[!!!] CRITICAL: RAM Limit Reached after contraction ({final_ram:.2f} GB)"
                )
                break

    except MemoryError:
        print("\n[!!!] OS MEMORY ERROR CAUGHT.")
    except Exception as e:
        print(f"\n[Error] Simulation crashed: {e}")
    finally:
        print("-" * 60)
        print(f"MAXIMUM BOND DIMENSION ACHIEVED: chi = {max_chi}")
        print("SIMULATION HALTED.")
        print("=" * 60)


if __name__ == "__main__":
    import sys

    if sys.stdout.encoding != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    run_simulation()
