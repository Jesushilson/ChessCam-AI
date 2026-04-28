from torchvision import transforms
import cv2 as cv
import random
import os

augment = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.3, contrast=0.3),
    transforms.ToTensor()
])

def augment_class(class_folder, target_count):
    images = os.listdir(class_folder)
    current_count = len(images)
    
    if current_count >= target_count:
        print(f"Skipping {class_folder} - already has enough images")
        return
    
    needed = target_count - current_count
    print(f"Augmenting {class_folder}: {current_count} → {target_count}")
    
    i = 0
    while i < needed:
        # Pick a random existing image
        img_name = random.choice(images)
        img_path = os.path.join(class_folder, img_name)
        img = cv.imread(img_path)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        
        # Apply augmentation
        augmented = augment(img)
        augmented = (augmented.numpy() * 255).astype('uint8')
        augmented = augmented.transpose(1, 2, 0)
        augmented = cv.cvtColor(augmented, cv.COLOR_RGB2BGR)
        
        # Save with new name
        save_path = os.path.join(class_folder, f"aug_{i}_{img_name}")
        cv.imwrite(save_path, augmented)
        i += 1