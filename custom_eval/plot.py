import json 
import os 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from collections import defaultdict
from typing import Dict, List, Tuple, Set, Any

# Configuration
SCORE_NAMES = {
    "evaluations/milu": ("milu", "acc,none"),
    "evaluations/arc_c_indic": ("arc_c_indic", "acc,none"),
    "evaluations/boolq_indic": ("boolq_indic", "acc,none"),
    "evaluations/triviaqa_indic_mcq": ("triviaqa_indic_mcq", "acc,none"),
    "evaluations/mmlu": ("mmlu", "acc,none"),
    "evaluations/mmlu_indic": ("mmlu_indic", "acc,none"),
    "evaluations/mmlu_indic_roman": ("mmlu_indic_roman", "acc,none"),
    "evaluations/igb/xsum": ("igb_xsum", "chrf,none"),
    "evaluations/igb/xquad": ("igb_xquad", "f1,none"),
    "evaluations/igb/xorqa": ("igb_xorqa", "f1,none"),
    "evaluations/igb/flores_xxen": ("igb_flores_xxen", "chrf,none"),
    "evaluations/igb/flores_enxx": ("igb_flores_enxx", "chrf,none"),
}

MODEL_NAMES = {
    "llama": "Llama-3.1-8B-Instruct",
    "gemma": "gemma-3-12b-it"
}

# Style configuration
MARKERS = ['o', 's', 'p', 'h', 'P', 'X', '^', 'v', '>', '<', 'D', '*']
COLORS = ['#4285F4', '#EA4335', '#FBBC04', '#34A853', '#9C27B0', 
          '#FF6F00', '#00ACC1', '#009688', '#795548', '#607D8B',
          '#AB47BC', '#FF5722']

OUTPUT_DIR = "plots"


def setup_output_directory():
    """Create output directory if it doesn't exist"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def fix_dataset_name(dataset: str) -> str:
    """Fix dataset names for display"""
    dataset = dataset.split('/')[0] if '/' in dataset else dataset
    
    name_mapping = {
        "updesh_R": "updesh_R (Full)",
        "updesh_R_uniform_random_sample": "updesh_R (Sample)"
    }
    
    return name_mapping.get(dataset, dataset)


def parse_directory_name(dirname: str) -> Tuple[str, str, bool]:
    """Parse directory name to extract model name, dataset, and custom status"""
    is_custom = dirname.startswith("__")
    splits = dirname.split("__")
    
    if is_custom:
        model_name = MODEL_NAMES.get(splits[-2], splits[-2])
        dataset = fix_dataset_name(splits[-3])
    else:
        model_name = splits[-1]
        dataset = "Proprietary"
    
    return model_name, dataset, is_custom


def extract_model_family(model: str) -> str:
    """Extract model family from model name"""
    if '-' in model:
        return model.split('-')[0]
    
    for i, char in enumerate(model):
        if char.isdigit():
            return model[:i].rstrip()
    
    return model


def get_consistent_style_mapping(all_data: Dict[str, List[Tuple]]) -> Tuple[Dict, Dict, Dict]:
    """Get consistent color and marker mappings across all plots"""
    # Collect all unique models
    all_models = set()
    for rows in all_data.values():
        for row in rows:
            all_models.add(row[0])
    
    # Group by families
    model_families = defaultdict(list)
    model_to_family = {}
    
    for model in sorted(all_models):
        family = extract_model_family(model)
        model_families[family].append(model)
        model_to_family[model] = family
    
    # Assign styles
    family_marker_map = {}
    model_color_map = {}
    
    for i, (family, models) in enumerate(sorted(model_families.items())):
        family_marker_map[family] = MARKERS[i % len(MARKERS)]
        
        for j, model in enumerate(sorted(models)):
            color_idx = len(model_color_map)
            model_color_map[model] = COLORS[color_idx % len(COLORS)]
    
    return model_color_map, family_marker_map, model_to_family


def collect_data(base_dir: str, task: str, score_name: str) -> List[Tuple]:
    """Collect data for a specific task"""
    rows = []
    
    if not os.path.exists(base_dir):
        return rows
    
    for dirname in os.listdir(base_dir):
        model_name, dataset, is_custom = parse_directory_name(dirname)
        dirpath = os.path.join(base_dir, dirname)
        
        for fname in os.listdir(dirpath):
            if not fname.startswith("results_"):
                continue
            
            try:
                with open(os.path.join(dirpath, fname)) as f:
                    data = json.load(f)
                score = data["results"][task][score_name]
                rows.append((model_name, score, is_custom, model_name, dataset))
            except (KeyError, FileNotFoundError, json.JSONDecodeError):
                continue
    
    return rows


def collect_all_data() -> Dict[str, List[Tuple]]:
    """Collect data for all tasks"""
    all_data = {}
    for task_key, (task_name, score_name) in SCORE_NAMES.items():
        all_data[task_key] = collect_data(task_key, task_name, score_name)
    return all_data


def setup_axes(ax):
    """Common axes setup"""
    ax.grid(True, axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


def add_mean_line(ax, values: List[float]):
    """Add mean line to plot"""
    mean_val = np.mean(values)
    ax.axhline(mean_val, color='red', linestyle='--', linewidth=2, 
              alpha=0.7, label=f'Mean: {mean_val:.3f}')


def aggregate_model_scores(rows: List[Tuple]) -> Dict[str, Dict]:
    """Aggregate scores by model"""
    model_stats = defaultdict(lambda: {
        'scores': [], 
        'datasets': set(), 
        'is_custom': False
    })
    
    for model_name, score, is_custom, _, dataset in rows:
        model_stats[model_name]['scores'].append(score)
        model_stats[model_name]['datasets'].add(dataset)
        model_stats[model_name]['is_custom'] = is_custom
    
    # Calculate means
    for stats in model_stats.values():
        stats['mean_score'] = np.mean(stats['scores'])
    
    return dict(model_stats)


def plot_bar_subplot(ax, rows: List[Tuple], task_name: str, score_type: str, 
                     model_color_map: Dict, model_is_custom: Dict):
    """Plot a single bar subplot with horizontal bars"""
    if not rows:
        ax.text(0.5, 0.5, f"No data for {task_name}", 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_xticks([])
        ax.set_yticks([])
        return
    
    # Create dataset/model combinations and sort by score (ascending for bottom-to-top display)
    dataset_model_scores = []
    for model_name, score, is_custom, _, dataset in rows:
        dataset_model_scores.append((dataset, model_name, score, is_custom))
    
    # Sort by score ascending (so highest scores appear at top)
    dataset_model_scores.sort(key=lambda x: x[2])
    
    # Plot bars
    labels = []
    scores = []
    colors = []
    hatches = []
    
    for dataset, model, score, is_custom in dataset_model_scores:
        # Only add dataset prefix if it's proprietary
        if dataset == "Proprietary":
            labels.append(model)
        else:
            labels.append(f"{dataset}/{model}")
        
        scores.append(score)
        colors.append(model_color_map.get(model, '#808080'))
        
        # Determine hatch pattern
        if dataset.startswith("updesh"):
            hatches.append('\\\\')  # Backward diagonal lines for updesh datasets
        elif is_custom:
            hatches.append('///')  # Forward diagonal lines for custom models
        else:
            hatches.append(None)
    
    # Create horizontal bars
    y_positions = range(len(labels))
    bars = []
    for i, (score, color, hatch) in enumerate(zip(scores, colors, hatches)):
        bar = ax.barh(i, score, color=color, 
                      edgecolor='black', linewidth=1.5, alpha=0.8,
                      hatch=hatch)
        bars.extend(bar)
    
    # Add value labels
    for bar, score in zip(bars, scores):
        width = bar.get_width()
        ax.text(width + 0.001, bar.get_y() + bar.get_height()/2.,
               f'{score:.3f}', ha='left', va='center', fontsize=7)
    
    # Format
    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=6)
    ax.set_xlabel(score_type.split(",")[0].upper(), fontsize=9)
    ax.set_title(f"{task_name.upper()}", fontsize=10, fontweight='bold')
    
    # Add mean line (vertical for horizontal bars)
    if scores:
        mean_val = np.mean(scores)
        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                  alpha=0.7, label=f'Mean: {mean_val:.3f}')
    
    # Setup axes
    ax.grid(True, axis='x', alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust spacing
    ax.set_ylim(-0.5, len(labels) - 0.5)


def plot_scatter_subplot(ax, rows: List[Tuple], task: str, score_name: str,
                        model_color_map: Dict, family_marker_map: Dict, 
                        model_to_family: Dict):
    """Plot a single scatter subplot"""
    if not rows:
        ax.text(0.5, 0.5, f"No data for {task}", 
               ha='center', va='center', transform=ax.transAxes)
        ax.set_xticks([])
        ax.set_yticks([])
        return
    
    # Sort by dataset name
    unique_datasets = sorted(list(set([r[4] for r in rows])))
    dataset_to_x = {d: i for i, d in enumerate(unique_datasets)}
    
    # Plot points
    plotted_labels = set()
    all_scores = []
    
    for model_name, score, _, _, dataset in rows:
        x = dataset_to_x[dataset]
        family = model_to_family.get(model_name, model_name)
        marker = family_marker_map.get(family, 'o')
        color = model_color_map.get(model_name, '#000000')
        
        label = model_name if model_name not in plotted_labels else ""
        ax.scatter(x, score, c=[color], marker=marker, alpha=0.9, 
                  edgecolors='black', s=100, linewidth=1, label=label)
        plotted_labels.add(model_name)
        all_scores.append(score)
    
    # Format
    ax.axhline(np.mean(all_scores), color='grey', linestyle='--', 
              linewidth=1, alpha=0.7)
    ax.set_xticks(range(len(unique_datasets)))
    ax.set_xticklabels(unique_datasets, rotation=45, ha='right', fontsize=8)
    ax.set_ylabel(score_name.split(",")[0].upper(), fontsize=9)
    ax.set_title(f"{task.upper()}", fontsize=10, fontweight='bold')
    
    # Setup axes
    setup_axes(ax)
    
    # Y-axis padding
    y_min, y_max = ax.get_ylim()
    y_range = y_max - y_min
    ax.set_ylim(y_min - 0.05 * y_range, y_max + 0.05 * y_range)


def create_legend_handles(model_color_map: Dict, family_marker_map: Dict, 
                         model_to_family: Dict) -> Tuple[List, List]:
    """Create legend handles and labels"""
    handles, labels = [], []
    
    for model_name in sorted(model_color_map.keys()):
        family = model_to_family.get(model_name, model_name)
        marker = family_marker_map.get(family, 'o')
        color = model_color_map[model_name]
        
        handle = Line2D([0], [0], marker=marker, color='w', 
                       markerfacecolor=color, markersize=10, 
                       markeredgecolor='black', linewidth=0)
        handles.append(handle)
        labels.append(model_name)
    
    return handles, labels


def create_combined_scatter_plot(all_data: Dict, model_color_map: Dict, 
                                family_marker_map: Dict, model_to_family: Dict):
    """Create combined scatter plot with subplots"""
    n_tasks = len(SCORE_NAMES)
    fig, axes = plt.subplots(4, 3, figsize=(18, 15))
    axes = axes.flatten()
    
    # Plot each task
    for idx, (k, v) in enumerate(SCORE_NAMES.items()):
        if idx < len(axes):
            plot_scatter_subplot(axes[idx], all_data[k], v[0], v[1], 
                               model_color_map, family_marker_map, model_to_family)
    
    # Hide unused subplots
    for idx in range(n_tasks, len(axes)):
        axes[idx].axis('off')
    
    # Add legend
    handles, labels = create_legend_handles(model_color_map, family_marker_map, 
                                           model_to_family)
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, -0.05),
              ncol=5, fontsize=10, frameon=True, fancybox=True, shadow=True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "all_tasks_combined.pdf"), 
                bbox_inches='tight')
    plt.close()


def create_individual_bar_plots(all_data: Dict, model_color_map: Dict):
    """Create individual bar plots for each task with horizontal bars"""
    for task_key, (task_name, score_type) in SCORE_NAMES.items():
        rows = all_data[task_key]
        if not rows:
            continue
        
        # Create dataset/model combinations and sort
        dataset_model_scores = []
        model_is_custom = {}
        
        for model_name, score, is_custom, _, dataset in rows:
            dataset_model_scores.append((dataset, model_name, score, is_custom))
            model_is_custom[model_name] = is_custom
        
        # Sort by score ascending (so highest scores appear at top)
        dataset_model_scores.sort(key=lambda x: x[2])
        
        # Create figure - adjusted size for horizontal bars
        fig, ax = plt.subplots(figsize=(10, max(8, len(dataset_model_scores) * 0.4)))
        
        # Plot bars
        labels = []
        scores = []
        colors = []
        hatches = []
        
        for dataset, model, score, is_custom in dataset_model_scores:
            # Only add dataset prefix if it's proprietary
            if dataset == "Proprietary":
                labels.append(model)
            else:
                labels.append(f"{dataset}/{model}")
            
            scores.append(score)
            colors.append(model_color_map.get(model, '#808080'))
            
            # Determine hatch pattern
            if dataset.startswith("updesh"):
                hatches.append('\\\\')  # Backward diagonal lines for updesh datasets
            elif is_custom:
                hatches.append('//')  # Forward diagonal lines for custom models
            else:
                hatches.append(None)
        
        # Create horizontal bars
        y_positions = range(len(labels))
        bars = []
        for i, (score, color, hatch) in enumerate(zip(scores, colors, hatches)):
            bar = ax.barh(i, score, color=color, 
                          edgecolor='black', linewidth=1.5, alpha=0.8,
                          hatch=hatch, height=0.8)
            bars.extend(bar)
        
        # Add value labels
        for bar, score in zip(bars, scores):
            width = bar.get_width()
            ax.text(width + 0.001, bar.get_y() + bar.get_height()/2.,
                   f'{score:.3f}', ha='left', va='center', fontsize=9)
        
        # Format
        ax.set_yticks(y_positions)
        ax.set_yticklabels(labels, fontsize=10)
        ax.set_xlabel(score_type.split(",")[0].upper(), fontsize=12)
        ax.set_title(f"{task_name.upper()} - Performance Comparison", 
                    fontsize=14, fontweight='bold', pad=20)
        
        # Add mean line (vertical for horizontal bars)
        if scores:
            mean_val = np.mean(scores)
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                      alpha=0.7, label=f'Mean: {mean_val:.3f}')
        
        # Legend
        from matplotlib.patches import Patch
        legend_handles = []
        
        # Add mean line to legend if it exists
        if scores:
            legend_handles.append(ax.get_legend_handles_labels()[0][0])
        
        # Add hatch patterns to legend
        custom_patch = Patch(facecolor='gray', edgecolor='black', hatch='//', 
                           alpha=0.8, label='Custom Model')
        updesh_patch = Patch(facecolor='gray', edgecolor='black', hatch='\\\\', 
                           alpha=0.8, label='Updesh Dataset')
        
        legend_handles.extend([custom_patch, updesh_patch])
        ax.legend(handles=legend_handles, loc='lower right')
        
        # Setup axes
        ax.grid(True, axis='x', alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Adjust spacing
        ax.set_ylim(-0.5, len(labels) - 0.5)
        
        # Add some padding
        plt.gcf().subplots_adjust(left=0.25)  # More space for y-axis labels
        
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, f"{task_name}_bar_plot.pdf"), 
                   bbox_inches='tight', dpi=300)
        plt.close()


def create_combined_bar_plot(all_data: Dict, model_color_map: Dict):
    """Create combined bar plot with subplots (similar to scatter plot) with horizontal bars"""
    n_tasks = len(SCORE_NAMES)
    fig, axes = plt.subplots(4, 3, figsize=(20, 18))
    axes = axes.flatten()
    
    # Collect model custom status across all tasks
    model_is_custom = {}
    for rows in all_data.values():
        for _, _, is_custom, model_name, _ in rows:
            model_is_custom[model_name] = is_custom
    
    # Plot each task
    for idx, (k, v) in enumerate(SCORE_NAMES.items()):
        if idx < len(axes):
            plot_bar_subplot(axes[idx], all_data[k], v[0], v[1], 
                           model_color_map, model_is_custom)
    
    # Hide unused subplots
    for idx in range(n_tasks, len(axes)):
        axes[idx].axis('off')
    
    # Add legend
    from matplotlib.patches import Patch
    custom_patch = Patch(facecolor='gray', edgecolor='black', hatch='//', 
                        alpha=0.8, label='Custom Model')
    updesh_patch = Patch(facecolor='gray', edgecolor='black', hatch='\\\\', 
                        alpha=0.8, label='Updesh Dataset')
    fig.legend(handles=[custom_patch, updesh_patch], loc='lower center', 
              bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "all_tasks_bar_combined.pdf"), 
                bbox_inches='tight')
    plt.close()


def main():
    """Main execution function"""
    setup_output_directory()
    
    # Collect all data
    all_data = collect_all_data()
    
    # Get style mappings
    model_color_map, family_marker_map, model_to_family = get_consistent_style_mapping(all_data)
    
    # Create scatter plot
    create_combined_scatter_plot(all_data, model_color_map, family_marker_map, 
                               model_to_family)
    print("Scatter plot created successfully!")
    
    # Create bar plots
    create_individual_bar_plots(all_data, model_color_map)
    create_combined_bar_plot(all_data, model_color_map)
    print("Bar plots with hatching created successfully!")


if __name__ == "__main__":
    main()