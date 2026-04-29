from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import numpy as np



def plot_class_accuracy(all_labels, model_name ,all_preds, class_names):
    # Get per class accuracy
    report = classification_report(all_labels, all_preds, 
                                  target_names=class_names, 
                                  output_dict=True)
    
    # Extract recall for each class
    classes = []
    accuracies = []
    
    for class_name in class_names:
        classes.append(class_name)
        accuracies.append(report[class_name]['recall'])
    
    # Plot
    colors = ['green' if acc >= 0.8 else 'orange' if acc >= 0.6 else 'red' for acc in accuracies]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(classes, accuracies, color=colors)
    
    # Add percentage labels on top of each bar
    for bar, acc in zip(bars, accuracies):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{acc*100:.1f}%', ha='center', va='bottom', fontsize=9)
    
    # Create the graph
    plt.xlabel(f'Chess Piece Class - {model_name}')
    plt.ylabel('Recall (Per Class Accuracy)')
    plt.title('Per Class Accuracy of Piece Classifier')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, 1.1)
    plt.axhline(y=0.8, color='gray', linestyle='--', label='80% threshold')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_comparison(homemade_losses, homemade_accs, pretrained_losses, pretrained_accs):
    epochs = range(1, len(homemade_losses) + 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Loss comparison
    ax1.plot(epochs, homemade_losses, 'b-', label='Homemade CNN')
    ax1.plot(epochs, pretrained_losses, 'r-', label='ResNet18')
    ax1.set_title('Training Loss Comparison')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax1.grid(True)

    # Validation accuracy comparison
    ax2.plot(epochs, homemade_accs, 'b-', label='Homemade CNN')
    ax2.plot(epochs, pretrained_accs, 'r-', label='ResNet18')
    ax2.axhline(y=80, color='gray', linestyle='--', label='80% threshold')
    ax2.set_title('Validation Accuracy Comparison')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy %')
    ax2.legend()
    ax2.grid(True)

    # Create the graph
    plt.suptitle('Homemade CNN vs ResNet18', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

def plot_confusion_matrix(all_labels, all_preds, class_names, model_name):
    cm = confusion_matrix(all_labels, all_preds)
    
    # Normalize to percentages
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    im = ax.imshow(cm_normalized, interpolation='nearest', cmap=plt.cm.Blues)
    plt.colorbar(im)
    
    # Add labels
    ax.set_xticks(np.arange(len(class_names)))
    ax.set_yticks(np.arange(len(class_names)))
    ax.set_xticklabels(class_names, rotation=45, ha='right')
    ax.set_yticklabels(class_names)
    
    # Add numbers inside each cell
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            value = cm_normalized[i, j]
            color = 'white' if value > 0.5 else 'black'
            ax.text(j, i, f'{value:.0%}', ha='center', va='center', color=color, fontsize=8)
    
    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')
    ax.set_title(f'Confusion Matrix — {model_name}')
    plt.tight_layout()
    plt.show()