"""
MP4视频音频转录脚本
使用Whisper将MP4视频文件中的音频转录为文本
Video transcription module for converting audio/video to text and processing with AI
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

from regex import F


# def process(input_file, raw_text_output, processed_text_output):
#     """
#     Transcribe audio/video file and process the text
    
#     Args:
#         input_file (str): Path to the input audio or video file
#         raw_text_output (str): Path where the raw transcription should be saved
#         processed_text_output (str): Path where the processed text should be saved
    
#     Returns:
#         bool: True if processing was successful, False otherwise
#     """
#     try:
#         # This is a placeholder implementation
#         # In a real implementation, you would:
#         # 1. Use Whisper or similar to transcribe the audio/video
#         # 2. Process the transcription with an AI model to organize the content
#         # 3. Save both raw and processed versions to Word documents
        
#         # For now, we'll just create simple Word documents with placeholder data
#         from docx import Document
        
#         # Create raw transcription document
#         raw_doc = Document()
#         raw_doc.add_heading('Raw Transcription', 0)
#         raw_doc.add_paragraph(f'Input file: {input_file}')
#         raw_doc.add_paragraph('This is a placeholder for the raw transcription.')
#         raw_doc.add_paragraph('In a real implementation, this would contain the actual transcribed text.')
#         raw_doc.save(raw_text_output)
        
#         # Create processed document
#         processed_doc = Document()
#         processed_doc.add_heading('Processed Meeting Notes', 0)
#         processed_doc.add_paragraph(f'Input file: {input_file}')
#         processed_doc.add_paragraph('This is a placeholder for the AI-processed meeting notes.')
#         processed_doc.add_paragraph('In a real implementation, this would contain organized meeting notes.')
#         processed_doc.add_heading('Key Points', 1)
#         processed_doc.add_paragraph('• Placeholder for key point 1')
#         processed_doc.add_paragraph('• Placeholder for key point 2')
#         processed_doc.add_paragraph('• Placeholder for key point 3')
#         processed_doc.add_heading('Action Items', 1)
#         processed_doc.add_paragraph('• Placeholder for action item 1')
#         processed_doc.add_paragraph('• Placeholder for action item 2')
#         processed_doc.save(processed_text_output)
        
#         return True
#     except Exception as e:
#         print(f"Error during transcription processing: {e}")
#         return False



def find_mp4_files(input_dir):
    """
    遍历输入目录，查找所有MP4文件
    
    Args:
        input_dir (str): 输入目录路径
        
    Returns:
        list: MP4文件路径列表
    """
    mp4_files = []
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"错误: 输入目录不存在: {input_dir}")
        return mp4_files
    
    # 递归查找所有mp4文件
    for file_path in input_path.rglob("*.mp4"):
        mp4_files.append(str(file_path.absolute()))
    
    # 也查找MP4大写扩展名
    # for file_path in input_path.rglob("*.MP4"):
    #     mp4_files.append(str(file_path.absolute()))
    
    return mp4_files


def prepare_video_files(video_paths):
    """
    准备视频文件：重命名为简化名称
    
    Args:
        video_paths (list): 视频文件路径列表
        
    Returns:
        list: 包含(原始路径, 临时路径, 原始文件名, 简化文件名)的元组列表
    """
    file_info_list = []
    
    for video_path in video_paths:
        # 获取原始文件信息
        video_dir = os.path.dirname(video_path)
        original_filename = os.path.basename(video_path)
        filename_without_ext = os.path.splitext(original_filename)[0]
        file_extension = os.path.splitext(original_filename)[1]
        
        # 提取_之前的字符串作为字符串1
        if '_' in filename_without_ext:
            string1 = filename_without_ext.split('_')[0]
        else:
            string1 = filename_without_ext
        
        # 构建临时文件名
        temp_filename = string1 + file_extension
        temp_video_path = os.path.join(video_dir, temp_filename)
        
        file_info_list.append((video_path, temp_video_path, original_filename, temp_filename, filename_without_ext, string1))
    
    return file_info_list


def rename_files_for_processing(file_info_list):
    """
    将文件重命名为简化名称以便处理
    
    Args:
        file_info_list (list): 文件信息列表
        
    Returns:
        list: 成功重命名的文件信息列表
    """
    renamed_files = []
    
    for original_path, temp_path, original_name, temp_name, _, _ in file_info_list:
        try:
            if original_path != temp_path:
                # 如果临时文件已存在，先删除
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                os.rename(original_path, temp_path)
                print(f"文件已重命名: {original_name} -> {temp_name}")
            renamed_files.append((original_path, temp_path, original_name, temp_name))
        except Exception as e:
            print(f"重命名失败: {original_name} - {str(e)}")
    
    return renamed_files


def restore_original_names(renamed_files):
    """
    恢复文件的原始名称
    
    Args:
        renamed_files (list): 已重命名的文件信息列表
    """
    for original_path, temp_path, original_name, temp_name in renamed_files:
        try:
            if os.path.exists(temp_path) and temp_path != original_path:
                os.rename(temp_path, original_path)
                print(f"文件名已恢复: {temp_name} -> {original_name}")
        except Exception as e:
            print(f"恢复文件名失败: {temp_name} - {str(e)}")


def process(input_file, raw_text_output, processed_text_output):
    #     """
    #     Transcribe audio/video file and process the text
        
    #     Args:
    #         input_file (str): Path to the input audio or video file
    #         raw_text_output (str): Path where the raw transcription should be saved
    #         processed_text_output (str): Path where the processed text should be saved
        
    #     Returns:
    #         bool: True if processing was successful, False otherwise
    #     """
    print(f"process({input_file},{raw_text_output},{processed_text_output})...")

    #将input_file拆分为路径和文件名
    input_path, input_filename = os.path.split(input_file)

    # 将input_filename按. 进行拆分为文件名称和扩展名
    input_name, input_extension = os.path.splitext(input_filename)

    # 将raw_text_output拆分为路径和文件名
    raw_text_path, raw_text_filename = os.path.split(raw_text_output)

    if transcribe_video(input_file, raw_text_path) == True:
        # 将结果写入raw_text_output
        write_text_to_file(raw_text_path + "\\" + input_name + ".txt", raw_text_output)

        # process_text(raw_text_path, processed_text_path)


    return True


def write_text_to_file(source_path, destination_path):
    """
    Copy text content from source file to destination file
    
    Args:
        source_path (str): Path to the source text file
        destination_path (str): Path where the text should be copied to
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"write_text_to_file({source_path}, {destination_path})...")

    try:
        # Ensure the destination directory exists
        dest_dir = os.path.dirname(destination_path)
        if dest_dir:
            os.makedirs(dest_dir, exist_ok=True)
        
        # Copy the file content
        with open(source_path, 'r', encoding='utf-8') as src_file:
            content = src_file.read()
        
        with open(destination_path, 'w', encoding='utf-8') as dest_file:
            dest_file.write(content)
        
        return True
    except Exception as e:
        print(f"Error writing text to file: {e}")
        return False


def transcribe_video(input_file, output_dir):
    try:
        # 构建whisper命令，包含所有临时文件路径
        temp_paths = [input_file]
        
        cmd = [
            "whisper.exe",
            "--language", "Chinese",
            "--device=cuda",
            "--output_dir", output_dir,
            "--output_format", "txt"
        ] + temp_paths
        
        print(f"执行批量转录命令，包含 {len(temp_paths)} 个文件")
        print(f"命令: whisper.exe --language Chinese --device=cuda --output_dir {output_dir} --output_format txt [{input_file}]")
        
        # 执行whisper命令
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"✗ 转录失败")
            print(f"错误信息: {result.stderr}")
            return False
        
        print(f"✓ 转录成功")
                        
        return True
        
    except FileNotFoundError:
        print("错误: 找不到whisper.exe，请确保Whisper已正确安装并在PATH中")
        return False
    except Exception as e:
        print(f"批量转录过程中发生错误: {str(e)}")
        return False
    finally:
        # 恢复所有文件的原始名称
        return True


def transcribe_video_batch(video_paths, output_dir):
    """
    批量转录视频文件（一次处理多个文件）
    
    Args:
        video_paths (list): 视频文件路径列表
        output_dir (str): 输出目录路径
        
    Returns:
        tuple: (成功数量, 失败数量)
    """
    if not video_paths:
        return 0, 0
    
    print(f"\n开始批量处理 {len(video_paths)} 个文件...")
    
    # 准备文件信息
    file_info_list = prepare_video_files(video_paths)
    
    # 重命名文件
    renamed_files = rename_files_for_processing(file_info_list)
    
    try:
        # 构建whisper命令，包含所有临时文件路径
        temp_paths = [temp_path for _, temp_path, _, _ in renamed_files]
        
        cmd = [
            "whisper.exe",
            "--language", "Chinese",
            "--device=cuda",
            "--output_dir", output_dir,
            "--output_format", "txt"
        ] + temp_paths
        
        print(f"执行批量转录命令，包含 {len(temp_paths)} 个文件")
        print(f"命令: whisper.exe --language Chinese --device=cuda --output_dir {output_dir} --output_format txt [文件列表]")
        
        # 执行whisper命令
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"✗ 批量转录失败")
            print(f"错误信息: {result.stderr}")
            return 0, len(video_paths)
        
        print(f"✓ 批量转录成功")
        
        # 重命名输出的txt文件
        success_count = 0
        for original_path, temp_path, original_name, temp_name in renamed_files:
            try:
                # 获取文件信息
                filename_without_ext = os.path.splitext(original_name)[0]
                temp_name_without_ext = os.path.splitext(temp_name)[0]
                
                whisper_output_txt = os.path.join(output_dir, temp_name_without_ext + ".txt")
                final_output_txt = os.path.join(output_dir, filename_without_ext + ".txt")
                
                if os.path.exists(whisper_output_txt):
                    if whisper_output_txt != final_output_txt:
                        # 如果目标文件已存在，先删除
                        if os.path.exists(final_output_txt):
                            os.remove(final_output_txt)
                        os.rename(whisper_output_txt, final_output_txt)
                        print(f"输出文件已重命名: {temp_name_without_ext}.txt -> {filename_without_ext}.txt")
                    success_count += 1
                else:
                    print(f"警告: 未找到预期的输出文件: {whisper_output_txt}")
            except Exception as e:
                print(f"重命名输出文件失败: {original_name} - {str(e)}")
        
        return success_count, len(video_paths) - success_count
        
    except FileNotFoundError:
        print("错误: 找不到whisper.exe，请确保Whisper已正确安装并在PATH中")
        return 0, len(video_paths)
    except Exception as e:
        print(f"批量转录过程中发生错误: {str(e)}")
        return 0, len(video_paths)
    finally:
        # 恢复所有文件的原始名称
        restore_original_names(renamed_files)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="批量转录MP4视频文件中的音频为文本")
    parser.add_argument("input_dir", help="输入视频文件所在的文件夹")
    parser.add_argument("output_dir", help="输出文本文件的文件夹")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    output_dir = args.output_dir
    
    # 检查输入目录
    if not os.path.exists(input_dir):
        print(f"错误: 输入目录不存在: {input_dir}")
        sys.exit(1)
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 查找所有MP4文件
    print(f"正在扫描目录: {input_dir}")
    mp4_files = find_mp4_files(input_dir)
    
    if not mp4_files:
        print("未找到任何MP4文件")
        sys.exit(0)
    
    print(f"找到 {len(mp4_files)} 个MP4文件")
    
    if args.verbose:
        for file_path in mp4_files:
            print(f"  - {file_path}")
    
    # 批量转录 - 每50个文件为一组
    success_count = 0
    total_count = len(mp4_files)
    batch_size = 50
    
    # 将文件分组处理
    for i in range(0, total_count, batch_size):
        batch_files = mp4_files[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (total_count + batch_size - 1) // batch_size
        
        print(f"\n=== 处理第 {batch_num}/{total_batches} 批次 ({len(batch_files)} 个文件) ===")
        
        if args.verbose:
            for j, file_path in enumerate(batch_files):
                print(f"  [{i+j+1}/{total_count}] {os.path.basename(file_path)}")
        
        # 批量处理当前组的文件
        batch_success, batch_failed = transcribe_video_batch(batch_files, output_dir)
        success_count += batch_success
        
        print(f"第 {batch_num} 批次完成: 成功 {batch_success}/{len(batch_files)}, 失败 {batch_failed}/{len(batch_files)}")
    
    # 显示结果统计
    print(f"\n转录完成!")
    print(f"成功: {success_count}/{total_count}")
    print(f"失败: {total_count - success_count}/{total_count}")
    print(f"输出目录: {output_dir}")


if __name__ == "__main__":
    main()        