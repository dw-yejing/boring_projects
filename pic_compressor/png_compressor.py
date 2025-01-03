import numpy as np
from PIL import Image
import os

class PNGCompressor:
    def __init__(self):
        pass

    def convert_to_8bit(self, image):
        """将图像转换为8位调色板模式，保留透明度和颜色"""
        if image.mode == 'RGBA':
            # 获取alpha通道
            alpha = image.split()[3]
            
            # 二值化alpha通道
            mask = Image.eval(alpha, lambda a: 0 if a < 128 else 255)
            
            # 保留原始RGB颜色，只修改alpha通道
            image_array = np.array(image)
            image_array[..., 3] = np.array(mask)
            
            # 创建一个临时的RGB图像用于量化
            rgb_image = Image.fromarray(image_array[..., :3], 'RGB')
            
            # 使用中位切分法进行颜色量化，保留更多颜色细节
            converted = rgb_image.quantize(colors=255, method=2)
            
            # 获取量化后的调色板
            palette = converted.getpalette()
            
            # 创建新的调色板图像
            final_image = converted.copy()
            
            # 设置透明像素
            alpha_mask = np.array(mask) == 0
            if np.any(alpha_mask):
                # 将透明像素的索引设为255
                img_data = np.array(final_image)
                img_data[alpha_mask] = 255
                final_image = Image.fromarray(img_data)
                
                # 确保调色板的最后一个颜色是透明的
                if palette:
                    # 保持最后一个颜色接近原图中透明区域的颜色
                    transparent_color = image_array[alpha_mask][0][:3] if len(image_array[alpha_mask]) > 0 else [0, 0, 0]
                    palette[-3:] = transparent_color
                    final_image.putpalette(palette)
                    final_image.info['transparency'] = 255
            
            return final_image
        else:
            # 直接转换为8位调色板模式，使用中位切分法
            return image.quantize(colors=256, method=2)

    def compress(self, input_path, output_path=None):
        """
        使用8位调色板模式压缩PNG图像，保持透明度和颜色质量
        """
        if output_path is None:
            filename, ext = os.path.splitext(input_path)
            output_path = f"{filename}_compressed{ext}"

        # 加载图像
        image = Image.open(input_path)
        original_size = image.size
        
        # 转换为8位调色板模式
        image = self.convert_to_8bit(image)
        
        # 保存为PNG，使用最大压缩
        image.save(output_path, 'PNG', optimize=True, compress_level=9)
        
        # 验证尺寸没有改变
        if image.size != original_size:
            raise ValueError("Image size changed during compression!")
        
        # 返回压缩信息
        original_file_size = os.path.getsize(input_path)
        compressed_file_size = os.path.getsize(output_path)
        compression_ratio = (original_file_size - compressed_file_size) / original_file_size * 100
        
        return {
            'original_size': original_file_size,
            'compressed_size': compressed_file_size,
            'compression_ratio': compression_ratio,
            'image_size': image.size,
            'mode': image.mode
        }

if __name__ == '__main__':
    compressor = PNGCompressor()
    input_image = 'origin_camera.png'
    
    result = compressor.compress(input_image)
    print("\n压缩结果:")
    print("-" * 50)
    print(f"原始大小: {result['original_size']/1024:.2f} KB")
    print(f"压缩后大小: {result['compressed_size']/1024:.2f} KB")
    print(f"压缩率: {result['compression_ratio']:.2f}%")
    print(f"图像尺寸: {result['image_size']}")
    print(f"颜色模式: {result['mode']}") 