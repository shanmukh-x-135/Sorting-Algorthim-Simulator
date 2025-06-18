import pygame
import random

# Constants
WIDTH, HEIGHT = 800, 600
NUM_BARS = 100
BAR_WIDTH = WIDTH // NUM_BARS

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
LIGHT_BLUE = (173, 216, 230)  # Light blue for background
DARK_BLUE = (255, 25, 112)     # Dark blue for accent

# Initialize pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algorithm Visualizer")
FONT_LARGE = pygame.font.SysFont('comicsans', 48)
FONT_MEDIUM = pygame.font.SysFont('comicsans', 36)
FONT_SMALL = pygame.font.SysFont('comicsans', 24)

# Global variables
def reset_array():
    global array, bar_color
    array = [random.randint(10, HEIGHT - 70) for _ in range(NUM_BARS)]
    bar_color = [BLUE] * NUM_BARS

reset_array()

def draw_array(algo_name):
    WIN.fill(LIGHT_BLUE)  # Background color
    if len(array) != len(bar_color):
        return
    for i in range(NUM_BARS):
        pygame.draw.rect(WIN, bar_color[i], (i * BAR_WIDTH, HEIGHT - array[i], BAR_WIDTH, array[i]))
    
    # Display the current algorithm name centered horizontally
    text_algo = FONT_MEDIUM.render(f"Algorithm: {algo_name}", True, DARK_BLUE)
    text_rect = text_algo.get_rect(center=(WIDTH // 2, 50))
    WIN.blit(text_algo, text_rect)
    
    pygame.display.update()

def display_instructions():
    WIN.fill(LIGHT_BLUE)  # Background color
    title = FONT_LARGE.render("Instructions", True, DARK_BLUE)
    WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    
    instructions = [
        "Press SPACE to start sorting",
        "Press R to reset the array",
        "Press UP/DOWN to change the algorithm",
        "Press I to toggle instructions"
    ]
    
    line_height = 50
    for idx, line in enumerate(instructions):
        text_instr = FONT_SMALL.render(line, True, DARK_BLUE)
        WIN.blit(text_instr, (WIDTH // 2 - text_instr.get_width() // 2, 150 + idx * line_height))

    pygame.display.update()

def bubble_sort():
    global bar_color
    for i in range(len(array) - 1):
        for j in range(len(array) - 1 - i):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                bar_color[j], bar_color[j + 1] = RED, GREEN
                yield
                bar_color[j], bar_color[j + 1] = BLUE, BLUE

def selection_sort():
    global bar_color
    for i in range(len(array)):
        min_idx = i
        for j in range(i + 1, len(array)):
            if array[j] < array[min_idx]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]
        bar_color[i], bar_color[min_idx] = GREEN, RED
        yield
        bar_color[i], bar_color[min_idx] = BLUE, BLUE

def insertion_sort():
    global bar_color
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            bar_color[j], bar_color[j + 1] = RED, GREEN
            yield
            bar_color[j], bar_color[j + 1] = BLUE, BLUE
            j -= 1
        array[j + 1] = key

def merge_sort(start, end):
    if end - start > 1:
        yield from merge_sort(start, (start + end) // 2)
        yield from merge_sort((start + end) // 2, end)
        merged = []
        left, right = start, (start + end) // 2
        while left < (start + end) // 2 and right < end:
            if array[left] < array[right]:
                merged.append(array[left])
                left += 1
            else:
                merged.append(array[right])
                right += 1
        while left < (start + end) // 2:
            merged.append(array[left])
            left += 1
        while right < end:
            merged.append(array[right])
            right += 1
        for i, sorted_val in enumerate(merged):
            array[start + i] = sorted_val
            bar_color[start + i] = GREEN
            yield
            bar_color[start + i] = BLUE

def quick_sort(start, end):
    if start < end:
        pivot = array[end]
        p_index = start
        for i in range(start, end):
            if array[i] < pivot:
                array[i], array[p_index] = array[p_index], array[i]
                bar_color[i], bar_color[p_index] = RED, GREEN
                yield
                bar_color[i], bar_color[p_index] = BLUE, BLUE
                p_index += 1
        array[p_index], array[end] = array[end], array[p_index]
        yield from quick_sort(start, p_index - 1)
        yield from quick_sort(p_index + 1, end)

def heapify(n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and array[i] < array[left]:
        largest = left

    if right < n and array[largest] < array[right]:
        largest = right

    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        bar_color[i], bar_color[largest] = RED, GREEN
        yield
        bar_color[i], bar_color[largest] = BLUE, BLUE
        yield from heapify(n, largest)

def heap_sort():
    global bar_color
    n = len(array)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)

    for i in range(n-1, 0, -1):
        array[i], array[0] = array[0], array[i]
        bar_color[i], bar_color[0] = RED, GREEN
        yield
        bar_color[i], bar_color[0] = BLUE, BLUE
        yield from heapify(i, 0)

def shell_sort():
    global bar_color
    n = len(array)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = array[i]
            j = i
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                bar_color[j], bar_color[j - gap] = RED, GREEN
                yield
                bar_color[j], bar_color[j - gap] = BLUE, BLUE
                j -= gap
            array[j] = temp
        gap //= 2

def counting_sort(exp):
    n = len(array)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = array[i] // exp
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = array[i] // exp
        output[count[index % 10] - 1] = array[i]
        count[index % 10] -= 1
        i -= 1

    for i in range(len(array)):
        array[i] = output[i]
        bar_color[i] = GREEN
        yield
        bar_color[i] = BLUE

def radix_sort():
    max_val = max(array)
    exp = 1
    while max_val // exp > 0:
        yield from counting_sort(exp)
        exp *= 10

def bucket_sort():
    max_val = max(array)
    size = max_val // len(array)

    buckets = [[] for _ in range(len(array))]

    for i in range(len(array)):
        j = min(len(array) - 1, array[i] // size)
        buckets[j].append(array[i])
        bar_color[i] = RED
        yield
        bar_color[i] = BLUE

    array.clear()
    for bucket in buckets:
        for value in sorted(bucket):
            array.append(value)
            bar_color[len(array) - 1] = GREEN
            yield
            bar_color[len(array) - 1] = BLUE

def comb_sort():
    global bar_color
    n = len(array)
    gap = n
    swapped = True

    while gap != 1 or swapped:
        gap = max(1, (gap * 10) // 13)
        swapped = False

        for i in range(n - gap):
            if array[i] > array[i + gap]:
                array[i], array[i + gap] = array[i + gap], array[i]
                bar_color[i], bar_color[i + gap] = RED, GREEN
                yield
                bar_color[i], bar_color[i + gap] = BLUE, BLUE
                swapped = True

# Main function
def main():
    global array, algo_index
    run = True
    clock = pygame.time.Clock()
    sorting = False
    sorting_algorithm = None
    sorting_algo_gen = None
    algos = [
        bubble_sort, selection_sort, insertion_sort,
        lambda: merge_sort(0, len(array)),
        lambda: quick_sort(0, len(array)-1),
        heap_sort, shell_sort, radix_sort, bucket_sort, comb_sort
    ]
    algo_names = [
        "Bubble Sort", "Selection Sort", "Insertion Sort",
        "Merge Sort", "Quick Sort", "Heap Sort", "Shell Sort",
        "Radix Sort", "Bucket Sort", "Comb Sort"
    ]
    algo_index = 0
    show_instructions = True

    while run:
        clock.tick(60)
        
        if show_instructions:
            display_instructions()
        else:
            draw_array(algo_names[algo_index])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sorting_algorithm = algos[algo_index]()
                    sorting_algo_gen = sorting_algorithm

                if event.key == pygame.K_r:
                    reset_array()
                    sorting = False

                if event.key == pygame.K_UP and not sorting:
                    algo_index = (algo_index + 1) % len(algos)

                if event.key == pygame.K_DOWN and not sorting:
                    algo_index = (algo_index - 1) % len(algos)

                if event.key == pygame.K_i:
                    show_instructions = not show_instructions

        if sorting:
            try:
                next(sorting_algo_gen)
            except StopIteration:
                sorting = False

    pygame.quit()

if __name__ == "__main__":
    main()
