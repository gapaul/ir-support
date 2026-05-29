##  @file
#   @brief A function to create an ellipsoid
#
#   @author Ho Minh Quang Ngo, Gavin Paul
#   @date May 29, 2026

import numpy as np
import matplotlib.pyplot as plt
from typing import Union, Optional, Tuple, List

def make_ellipsoid(
    ellipsoid_info: Union[np.ndarray, List[float]],
    center: Union[np.ndarray, List[float]],
    color: Optional[str] = None,
    u: Optional[np.ndarray] = None,
    v: Optional[np.ndarray] = None,
    ax: Optional[plt.Axes] = None,
    is_plot: bool = True) -> Union[Tuple[plt.Axes, Tuple[np.ndarray, np.ndarray, np.ndarray]], Tuple[np.ndarray, np.ndarray, np.ndarray]]:
        """
        Simple custom function to create an ellipsoid.

        :param ellipsoid_info: 1x3 array-like (ellipsoid radii) or 3x3 array (inversion of the ellipsoid matrix)
        :param center: centre of the ellipsoid
        :param color: colour for ellipsoid
        :param u: list of azimuthal angle in spherical coordinates (optional)
        :param v: list of polar angle in spherical coordinates (optional)
        :param ax: axis to plot on (optional)
        :return surface object & tuple of mesh data (X, Y, Z)
        """
        ellipsoid_info = np.asarray(ellipsoid_info, dtype=float)
        center = np.asarray(center, dtype=float)

        if np.shape(ellipsoid_info) == (1, 3) or np.shape(ellipsoid_info) == (3,):
            lengths = ellipsoid_info.reshape(3)
            eigenvectors = np.eye(3)
        elif np.shape(ellipsoid_info) == (3, 3):
            eigenvalues, eigenvectors = np.linalg.eig(ellipsoid_info)
            lengths = np.sqrt(np.abs(eigenvalues))
        else:
            raise ValueError('Invalid input ellipsoid info!')

        # Ellipsoid surface
        if u is None:
            u = np.linspace(0, 2 * np.pi, 100)
        if v is None:
            v = np.linspace(0, np.pi, 50)

        # Generate surface points of the ellipsoid
        phi, theta = np.meshgrid(u, v, indexing='ij')
        local_points = np.stack((
            lengths[0] * np.cos(phi) * np.sin(theta),
            lengths[1] * np.sin(phi) * np.sin(theta),
            lengths[2] * np.cos(theta)
        ), axis=-1)
        rotated_points = local_points @ eigenvectors.T
        X = rotated_points[:, :, 0] + center[0]
        Y = rotated_points[:, :, 1] + center[1]
        Z = rotated_points[:, :, 2] + center[2]

        if is_plot:
            # Plot ellipsoid
            if ax is None:
                ax = plt.figure().add_subplot(projection='3d')

            if color is None:
                return ax.plot_surface(X, Y, Z, cmap='inferno', alpha=0.5), (X,Y,Z)

            return ax.plot_surface(X, Y, Z, color=color, alpha=0.5), (X,Y,Z)

        else:
            return (X,Y,Z)
