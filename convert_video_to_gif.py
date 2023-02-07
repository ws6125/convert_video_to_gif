import argparse
import imageio
import os

from pathlib import Path
# from tqdm import tqdm

def convert_to_gif(input_path, output_path, fps = None):
    if not os.path.exists(input_path):
        raise Exception('Video file not exists!!')
    elif Path(input_path).suffix not in ['.mp4', '.wmv', '.avi', '.mov']:
        raise Exception('Unsupport file format!!')

    reader = imageio.get_reader(input_path)
    if fps is None:
        fps = reader.get_meta_data()['fps']

    Path(output_path).parent.mkdir(parents = True, exist_ok = True)
    if '.gif' != Path(output_path).suffix:
        output_path += '.gif'

    writer = imageio.get_writer(output_path, fps = fps)
    for frame in reader:
        writer.append_data(frame)
    writer.close()


if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type = str, help = 'video path')
    parser.add_argument('--output', type = str, help = 'output path')
    parser.add_argument('--fps', type = int, default = 0, help = 'fps of gif, 0 means default')
    opt = parser.parse_args()

    convert_to_gif(opt.input, opt.output, fps = opt.fps if (0 != opt.fps) else None)

