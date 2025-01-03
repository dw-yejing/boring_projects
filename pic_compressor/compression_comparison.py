import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import cv2
from png_compressor import PNGCompressor
import skimage.io
import imageio
import png
from skimage import img_as_ubyte
from skimage.color import rgb2lab, lab2rgb
from skimage.transform import resize

def get_file_size_kb(path):
    """Return file size in KB"""
    return os.path.getsize(path) / 1024

def compare_compression_methods(input_image_path):
    """Compare different compression methods and return their results"""
    results = []
    original_size = get_file_size_kb(input_image_path)
    image = Image.open(input_image_path)
    
    # 创建compare文件夹（如果不存在）
    compare_dir = 'compare'
    os.makedirs(compare_dir, exist_ok=True)
    
    # 获取文件名（不含路径）并添加compare路径
    base_name = os.path.splitext(os.path.basename(input_image_path))[0]
    base_path = os.path.join(compare_dir, base_name)

    # 1. Custom 8-bit palette compression
    custom_compressor = PNGCompressor()  # 创建压缩器实例
    custom_output = f"{base_path}_custom_compressed.png"
    custom_result = custom_compressor.compress(input_image_path, custom_output)
    results.append({
        'method': 'Ours',
        'size': custom_result['compressed_size'] / 1024,
        'ratio': custom_result['compression_ratio']
    })

    # 2. PIL's default PNG compression (optimize=True)
    pil_output = f"{base_path}_pil_optimized.png"
    image.save(pil_output, 'PNG', optimize=True)
    pil_size = get_file_size_kb(pil_output)
    results.append({
        'method': 'PIL',
        'size': pil_size,
        'ratio': (original_size - pil_size) / original_size * 100
    })

    # 3. OpenCV PNG compression
    cv_image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)  # 保持原始通道
    if len(cv_image.shape) == 3 and cv_image.shape[2] == 4:  # 如果是RGBA图像
        # 保持RGBA格式，不转换为BGR
        pass
    elif len(cv_image.shape) == 3 and cv_image.shape[2] == 3:  # 如果是RGB图像
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2BGRA)  # 转换为BGRA
    
    for compression in [5, 9]:  # OpenCV的PNG压缩级别
        cv_output = f"{base_path}_opencv_comp{compression}.png"
        cv2.imwrite(cv_output, cv_image, [
            cv2.IMWRITE_PNG_COMPRESSION, compression,
            cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
        ])
        cv_size = get_file_size_kb(cv_output)
        results.append({
            'method': f'OpenCV (Level {compression})',
            'size': cv_size,
            'ratio': (original_size - cv_size) / original_size * 100
        })

    # 4. Scikit-image compression
    ski_image = skimage.io.imread(input_image_path)
    ski_output = f"{base_path}_skimage.png"
    skimage.io.imsave(ski_output, ski_image, check_contrast=False)
    ski_size = get_file_size_kb(ski_output)
    results.append({
        'method': 'Scikit-image',
        'size': ski_size,
        'ratio': (original_size - ski_size) / original_size * 100
    })

    # 5. Imageio compression
    img = imageio.imread(input_image_path)
    imageio_output = f"{base_path}_imageio.png"
    imageio.imwrite(imageio_output, img, format='png', optimize=True)
    imageio_size = get_file_size_kb(imageio_output)
    results.append({
        'method': 'Imageio',
        'size': imageio_size,
        'ratio': (original_size - imageio_size) / original_size * 100
    })

    # 6. PyPNG compression
    # 使用PIL来获取正确的像素数据
    pil_image = Image.open(input_image_path)
    width, height = pil_image.size
    
    # 保持RGBA模式
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')
    
    # 获取像素数据，包括alpha通道
    pixel_data = list(pil_image.getdata())
    
    # 转换为PyPNG期望的格式，包括alpha通道
    pixel_list = []
    for y in range(height):
        row = []
        for x in range(width):
            pixel = pixel_data[y * width + x]
            row.extend(pixel)  # 现在pixel包含RGBA四个通道
        pixel_list.append(row)
    
    # 写入PNG文件，设置alpha=True
    pypng_output = f"{base_path}_pypng.png"
    output_file = open(pypng_output, 'wb')
    writer = png.Writer(
        width=width,
        height=height,
        bitdepth=8,
        greyscale=False,
        alpha=True,  # 启用alpha通道
        compression=9
    )
    writer.write(output_file, pixel_list)
    output_file.close()
    pypng_size = get_file_size_kb(pypng_output)
    results.append({
        'method': 'PyPNG',
        'size': pypng_size,
        'ratio': (original_size - pypng_size) / original_size * 100
    })

    return results, original_size

def plot_compression_comparison(results, original_size):
    """Create visualization of compression results"""
    methods = [r['method'] for r in results]
    ratios = [r['ratio'] for r in results]

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 创建图表
    plt.figure(figsize=(12, 8))
    
    # 设置柱状图颜色
    colors = ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f', '#9b59b6', '#1abc9c']
    bars = plt.bar(methods, ratios, color=colors)
    
    # 设置标题和标签
    plt.title('Compression Ratio Comparison', fontsize=14, pad=20)
    plt.ylabel('Compression Ratio (%)', fontsize=12)
    plt.xlabel('Compression Methods', fontsize=12)
    
    # 调整x轴标签
    plt.xticks(rotation=30, ha='right')
    
    # 添加网格线使数据更易读
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 在柱状图上添加数值标签
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom',
                fontsize=10)
    
    # 调整布局
    plt.tight_layout()
    
    # 确保compare文件夹存在
    os.makedirs('compare', exist_ok=True)
    
    # 保存图表到compare文件夹
    plt.savefig(os.path.join('compare', 'compression_ratio_comparison.png'), dpi=300, bbox_inches='tight')
    plt.show()
    plt.close()

def plot_image_comparison(input_image_path, results):
    """Create a visual comparison of all compressed images"""
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 计算需要的行数和列数
    n_images = len(results) + 1  # +1 for original image
    n_cols = 4  # 每行4张图片
    n_rows = (n_images + n_cols - 1) // n_cols

    # 创建图表
    fig = plt.figure(figsize=(15, 5 * n_rows))
    
    # 显示原图
    plt.subplot(n_rows, n_cols, 1)
    original = plt.imread(input_image_path)
    plt.imshow(original)
    plt.text(0.02, 0.98, f'Original    {os.path.getsize(input_image_path)/1024:.1f}KB',
             horizontalalignment='left',
             verticalalignment='top',
             transform=plt.gca().transAxes,
             fontsize=9,
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=3))
    plt.axis('off')

    # 显示压缩后的图片
    label_dict = {
        'Ours': 'origin_camera_custom_compressed.png',
        'PIL': 'origin_camera_pil_optimized.png',
        'OpenCV (Level 5)': 'origin_camera_opencv_comp5.png',
        'OpenCV (Level 9)': 'origin_camera_opencv_comp9.png',
        'Scikit-image': 'origin_camera_skimage.png',
        'Imageio': 'origin_camera_imageio.png',
        'PyPNG': 'origin_camera_pypng.png'
    }
    for idx, result in enumerate(results, 2):
        plt.subplot(n_rows, n_cols, idx)
        # 从compare文件夹中读取对应的图片
        img_path = label_dict[result['method']]
        img = plt.imread(os.path.join('compare', img_path))
        plt.imshow(img)
        plt.text(0.02, 0.98, f"{result['method']}    {result['size']:.1f}KB    Ratio: {result['ratio']:.1f}%",
                horizontalalignment='left',
                verticalalignment='top',
                transform=plt.gca().transAxes,
                fontsize=9,
                bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=3))
        plt.axis('off')

    # 调整布局
    plt.tight_layout()
    
    # 保存对比图
    plt.savefig(os.path.join('compare', 'visual_comparison.png'), 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    plt.show()
    plt.close()

if __name__ == '__main__':
    input_image = 'origin_camera.png'
    results, original_size = compare_compression_methods(input_image)
    
    # 打印结果
    print("\nCompression Results Comparison:")
    print("-" * 50)
    print(f"Original Size: {original_size:.2f} KB")
    for result in results:
        print(f"\n{result['method']}:")
        print(f"Compressed Size: {result['size']:.2f} KB")
        print(f"Compression Ratio: {result['ratio']:.2f}%")
    
    # 生成压缩率对比图表
    plot_compression_comparison(results, original_size)
    
    # 生成图片视觉对比
    plot_image_comparison(input_image, results) 