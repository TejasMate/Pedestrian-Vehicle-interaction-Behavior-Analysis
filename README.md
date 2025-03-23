# Pedestrian Interaction Behavior Analysis

This project analyzes both pedestrian and vehicle interaction behavior in various traffic scenarios using advanced data analysis and machine learning techniques. It processes and visualizes movement data of pedestrians and vehicles from different locations including intersections, roundabouts, and merging zones. The analysis includes vehicle tracking, speed patterns, and safety implications of pedestrian-vehicle interactions.

## Key Features

### Data Processing & Visualization
- Map visualization of different traffic scenarios
- Vehicle and pedestrian trajectory tracking and visualization
- Speed analysis and movement patterns for both vehicles and pedestrians
- Comprehensive interaction detection between pedestrians and vehicles
- Vehicle behavior analysis in different traffic contexts

### Machine Learning Components

#### 1. Trajectory Prediction
- Implements machine learning models to predict both vehicle and pedestrian movement patterns
- Uses historical trajectory data to forecast future positions of all traffic participants
- Considers environmental factors, vehicle dynamics, and interaction contexts

#### 2. Interaction Classification
- Categorizes different types of pedestrian-vehicle interactions
- Identifies behavioral patterns of both vehicles and pedestrians in various scenarios
- Analyzes interaction outcomes, risk assessment, and safety implications
- Studies vehicle behavior adaptation in presence of pedestrians

#### 3. Pattern Recognition
- Clustering analysis for identifying common behavioral patterns of vehicles and pedestrians
- Scenario-specific pattern analysis (intersections, roundabouts, merging zones)
- Temporal pattern detection in vehicle and pedestrian movements
- Analysis of vehicle-pedestrian interaction patterns in different traffic conditions

#### 4. Risk Assessment
- Machine learning models for evaluating potential conflict situations
- Real-time risk level prediction
- Historical data-based risk pattern analysis

#### 5. Feature Engineering Pipeline
- Automated feature extraction from tracking data
- Preprocessing pipeline for machine learning models
- Feature selection and importance analysis

## Project Structure

- `maps/`: Contains OSM map files for different locations
- `recorded_trackfiles/`: Contains trajectory data files
- `*.py`: Python scripts for various analysis components

## Dependencies

- Python 3.x
- Matplotlib
- Pandas
- NumPy
- PyProj
- XML ElementTree

## Usage

1. Ensure all dependencies are installed
2. Place map files in the `maps/` directory
3. Place tracking data in the `recorded_trackfiles/` directory
4. Run the desired analysis scripts

## Future Enhancements

- Deep learning models for complex pattern recognition
- Real-time prediction system
- Interactive visualization dashboard
- Extended scenario coverage
- Integration with traffic management systems
