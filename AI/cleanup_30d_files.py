import os
import time
import datetime

def cleanup_old_files(target_dir, days_threshold=30):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"delete30_{timestamp}.txt"
    
    files_to_delete = []
    empty_dirs_to_delete = []
    
    current_time = time.time()
    seconds_threshold = days_threshold * 86400

    # 1. 查找超过30天的文件
    for root, dirs, files in os.walk(target_dir):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                file_age = current_time - os.path.getmtime(file_path)
                if file_age > seconds_threshold:
                    files_to_delete.append(file_path)
            except OSError as e:
                print(f"无法访问文件 {file_path}: {e}")

    # 打印文件清单并确认
    if files_to_delete:
        print("\n--- 准备删除的文件清单 (超过30天) ---")
        for f in files_to_delete:
            print(f)
        
        confirm = input(f"\n确定要删除以上 {len(files_to_delete)} 个文件吗？(y/n): ")
        if confirm.lower() == 'y':
            deleted_files = []
            for f in files_to_delete:
                try:
                    os.remove(f)
                    deleted_files.append(f)
                    print(f"已删除文件: {f}")
                except OSError as e:
                    print(f"删除失败 {f}: {e}")
            files_to_delete = deleted_files
        else:
            print("文件删除操作已取消。")
            files_to_delete = []
    else:
        print("未发现超过30天的文件。")

    # 2. 检查空目录 (自底向上遍历)
    for root, dirs, files in os.walk(target_dir, topdown=False):
        if not os.listdir(root) and root != target_dir:
            empty_dirs_to_delete.append(root)

    # 打印空目录清单并确认
    if empty_dirs_to_delete:
        print("\n--- 准备删除的空目录清单 ---")
        for d in empty_dirs_to_delete:
            print(d)
        
        confirm = input(f"\n确定要删除以上 {len(empty_dirs_to_delete)} 个空目录吗？(y/n): ")
        if confirm.lower() == 'y':
            deleted_dirs = []
            for d in empty_dirs_to_delete:
                try:
                    os.rmdir(d)
                    deleted_dirs.append(d)
                    print(f"已删除目录: {d}")
                except OSError as e:
                    print(f"删除失败 {d}: {e}")
            empty_dirs_to_delete = deleted_dirs
        else:
            print("目录删除操作已取消。")
            empty_dirs_to_delete = []
    else:
        print("未发现空目录。")

    # 3. 输出到日志文件
    with open(log_filename, 'w', encoding='utf-8') as log_file:
        log_file.write(f"清理时间: {datetime.datetime.now()}\n")
        log_file.write(f"目标目录: {target_dir}\n")
        log_file.write("-" * 50 + "\n")
        log_file.write("已删除的文件清单:\n")
        if files_to_delete:
            for f in files_to_delete:
                log_file.write(f"{f}\n")
        else:
            log_file.write("(无)\n")
            
        log_file.write("\n已删除的空目录清单:\n")
        if empty_dirs_to_delete:
            for d in empty_dirs_to_delete:
                log_file.write(f"{d}\n")
        else:
            log_file.write("(无)\n")
            
    print(f"\n处理完成。清单已保存至: {log_filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python cleanup_old_files.py <目标目录>")
    else:
        target = sys.argv[1]
        if os.path.isdir(target):
            cleanup_old_files(os.path.abspath(target))
        else:
            print(f"错误: {target} 不是有效的目录。")
