import pygame as pg

def create_texture():
    pg.init()
    surf = pg.Surface((256, 256))
    
    # 1. Yellow and Black diagonal stripes (Top half)
    # Fill with yellow
    surf.fill((255, 255, 0), (0, 0, 256, 128))
    # Draw black stripes
    stripe_width = 20
    for i in range(-256, 512, stripe_width * 2):
        pg.draw.polygon(surf, (0, 0, 0), [
            (i, 0), (i + stripe_width, 0),
            (i + stripe_width + 128, 128), (i + 128, 128)
        ])
        
    # 2. Red and White stripes (Bottom half) for Crossbuck
    # Fill with white
    surf.fill((255, 255, 255), (0, 128, 256, 128))
    # Draw red stripes
    for i in range(0, 256, stripe_width * 2):
        pg.draw.rect(surf, (255, 0, 0), (i, 128, stripe_width, 128))
    
    # Add black border to crossbuck section
    pg.draw.rect(surf, (0, 0, 0), (0, 128, 256, 128), 4)
        
    pg.image.save(surf, "textured_signal.png")
    print("Texture 'textured_signal.png' created.")

if __name__ == "__main__":
    create_texture()
