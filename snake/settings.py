# WINDOW INFORMATION
WINDOW_SIZE = 800, 600
FIELDS = 20, 15

# MOVEMENT.
START_POSITION = 5, FIELDS[1] // 2
DIRECTIONS = {'LEFT': (-1, 0), 'RIGHT': (1, 0), 'UP': (0, -1), 'DOWN': (0, 1)}
REFRESH_SPEED = 250

# FIELDS LIMITS.
LEFT_LIMIT = TOP_LIMIT = 0
RIGHT_LIMIT = FIELDS[0]
BOTTOM_LIMIT = FIELDS[1]

# COLORS.
SNAKE_BODY_COLOR = '#8EF249'
SNAKE_HEAD_COLOR = '#71CC1D'
APPLE_COLOR = '#F9473E'
