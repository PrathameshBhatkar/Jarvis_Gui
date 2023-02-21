import pygame


def load_sprite_sheet(sprite_sheet, number_of_columns, number_of_rows, width_of_one_image, height_of_one_image) -> list:
    if type(sprite_sheet) == type(''):
        sprite_sheet = pygame.image.load(sprite_sheet)

    if number_of_rows == 0:
        row0 = []

        for i in range(number_of_columns):
            i *= width_of_one_image
            cropped = (i, 0, i + width_of_one_image, height_of_one_image)
            s = pygame.Surface((width_of_one_image, height_of_one_image))
            print(cropped)

            s.blit(sprite_sheet, (0, 0), cropped)
            s.set_colorkey((0, 0, 0))

            row0.append(s)

        return row0
    else:
        load_multiple_rows_spritesheet(sprite_sheet, number_of_columns, number_of_rows, width_of_one_image,
                                       height_of_one_image)


def load_multiple_rows_spritesheet(sprite_sheet, number_of_columns, number_of_rows, width_of_one_image,
                                   height_of_one_image):
    l = [[]]*number_of_rows
    for x in range(number_of_rows):
        for i in range(number_of_columns):
            i *= width_of_one_image
            cropped = (i, 0, i + width_of_one_image, height_of_one_image)
            s = pygame.Surface((width_of_one_image, height_of_one_image))

            s.blit(sprite_sheet, (0, 0), cropped)
            s.set_colorkey((0, 0, 0))

            l[x].append(s)

    return l
