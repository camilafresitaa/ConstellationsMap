# ConstellationsMap
This project is a star and constellation visualizer built entirely with **matrix transformations**. It demonstrates how translation, rotation, scaling, reflection, and shearing can be applied using matrix multiplication.

![Constellations Map Banner](https://github.com/camilafresitaa/ConstellationsMap/blob/main/banner.jpg)

## Project Overview

**Constellations Map** visualizes stars from the Bright Star Catalog and draws recognized constellations based on HR numbers. It uses a **stereographic projection** to project the celestial sphere into 2D, and applies geometric transformations via 3x3 matrices to manipulate the star field interactively.

## Project Structure

```
main.py
 data/
    ├️ ybsc5
    └️ constellations.csv
 stars/
    ├️ stars.py
    ├️ stars_coords_2d.py
    └️ bsc_parser.py
 constellations/
    ├️ constellations.py
    └️ constellations_parser.py
 renderer/
    └️ draw.py
 scr/
    └️ transformations.py
 input/
    └️ events.py
```

- **`main.py`**: The entry point of the application. It initializes the window, loads the star and constellation data, handles user input, applies matrix transformations, and draws everything on screen.

- **`data/`**: Contains the raw input files.
  - `ybsc5`: The Yale Bright Star Catalogue in its original format.
  - `constellations.csv`: The custom dataset defining how to connect stars for each constellation.

- **`stars/`**: Responsible for reading and processing star data.
  - `bsc_parser.py`: Parses the BSC catalog.
  - `stars_coords_2d.py`: Projects celestial coordinates into 2D.
  - `stars.py`: Defines the Star class and manages star objects.

- **`constellations/`**: Manages constellation structure.
  - `constellations_parser.py`: Reads and parses the CSV file.
  - `constellations.py`: Defines Constellation objects and binds them to actual stars.

- **`renderer/`**: Contains `draw.py`, which handles drawing stars, constellation lines, names, and overlays.

- **`scr/`**: Contains `transformations.py`, where all transformation matrices (rotation, translation, scaling, shearing, reflection) are defined.

- **`input/`**: Contains `events.py`, which maps keyboard and mouse input to transformation states.

## Requirements

- Python 3
- Libraries:
  - `numpy`
  - `pygame`
  - `math`

## Running the Project

1. Clone this repository:
   
   ```
   git clone https://github.com/camilafresitaa/ConstellationsMap
   ```

2. Install the necessary libraries:

   ```
   pip install numpy
   pip install pygame
   ```

3. Run the `main.py` script:

   ```
   run main.py
   ```

## Features & Transformations

All transformations are implemented using **homogeneous coordinates** and **matrix multiplication only**:

| Transformation | Description |
|----------------|-------------|
| Rotation    | Rotate the star field by a given angle |
| Translation | Move the scene in x and y |
| Scaling     | Zoom in/out by scaling x and y |
| Reflection  | Mirror across x, y, or both axes |
| Shearing    | Tilt the scene using shear matrices |

## Controls

| Action                    | Key              |
|---------------------------|------------------|
| Rotate                    | `Q` / `E` or ← / → |
| Translate (move)          | `W`, `A`, `S`, `D` |
| Zoom in/out               | `+`, `-` or Mouse Wheel |
| Shear X / Y               | `Z` `X` / `C` `V` |
| Reflect over X / Y axis   | `F` / `G`         |
| Reset transformations     | `R`              |
| Toggle Help Overlay       | `H`              |
| Toggle Constellations     | `.`              |
| Toggle Constellation Names| `L`              |
| Toggle HR Labels          | `K`              |

Mouse Controls:
- **Left-click + drag** → Move the scene
- **Right-click + drag** → Rotate the scene

## Datasets Used

This project combines two datasets:

- **Yale Bright Star Catalogue (BSC5)**  
  Provided by the Yale University Observatory, this catalog contains over 9,000 stars with positions, magnitudes, and other metadata. It is used here to obtain the positional and brightness data of the stars.  
  [Catalog Reference](http://tdc-www.harvard.edu/catalogs/bsc5.html)

- **ConstellationsDataset**  
  A custom dataset created specifically for this project, containing the sequences of HR numbers used to draw the constellation lines. Each sequence defines how stars should be connected visually to form the classical constellation shapes.  
  [View on GitHub](https://github.com/camilafresitaa/ConstellationsDataset)

## Important Note

Some constellations, such as **Andromeda**, **Aquarius**, **Cetus**, **Pegasus**, **Pisces**, and **Sculptor**, are not visible in the current visualization.  
This is because an **angular distance limit** was applied to avoid severe distortions caused by the stereographic projection when moving too far from the center.

