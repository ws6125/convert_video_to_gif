import argparse
import cv2
import imageio
import os

from pathlib import Path

def convert_to_gif(input_path, output_path, fps = None, percentage = None):
    if not os.path.exists(input_path):
        raise Exception('Video file not exists!!')
    elif Path(input_path).suffix not in ['.mp4', '.wmv', '.avi', '.mov']:
        raise Exception('Unsupport file format!!')
    elif (percentage is not None) and ((1 < percentage) or (0 > percentage)):
        raise Exception('Percentage should be between 0 and 1!!')


    reader = imageio.get_reader(input_path)
    if fps is None:
        fps = reader.get_meta_data()['fps']

    if percentage is not None:
        width, height = reader.get_meta_data()['source_size']
        width *= percentage
        height *= percentage

    Path(output_path).parent.mkdir(parents = True, exist_ok = True)
    if '.gif' != Path(output_path).suffix:
        output_path += '.gif'

    writer = imageio.get_writer(output_path, fps = fps)
    for frame in reader:
        # Resize the frame
        if percentage is not None:
            frame = cv2.resize(frame, (int(width), int(height)))

        writer.append_data(frame)

    writer.close()


if '__main__' == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type = str, help = 'video path')
    parser.add_argument('--output', type = str, help = 'output path')
    parser.add_argument('--percentage', type = float, default = None, help = 'percentage of gif, should be between 0 and 1')
    parser.add_argument('--fps', type = int, default = 0, help = 'fps of gif, 0 means default')
    opt = parser.parse_args()

    convert_to_gif(
        opt.input,
        opt.output,
        fps = opt.fps if (0 != opt.fps) else None,
        percentage = opt.percentage,
    )
