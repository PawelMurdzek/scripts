#!/usr/bin/env python3
import json
import sys

def filter_packets_by_frame_number(input_file_path, output_file_path, max_frame_number=10000):
    """
    Reads JSON objects line-by-line from an input file, and writes them to an
    output file until a frame number greater than the max_frame_number is found.

    Args:
        input_file_path (str): The path to the input JSON Lines file.
        output_file_path (str): The path where the output will be saved.
        max_frame_number (int): The last frame number to include. Processing stops
                                after this frame.
    """
    print(f"Starting processing...")
    print(f"Input file: {input_file_path}")
    print(f"Output file: {output_file_path}")
    print(f"Will cut everything after frame number {max_frame_number}.")

    try:
        with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
            for line_num, line in enumerate(infile, 1):
                try:
                    # Attempt to load the line as a JSON object
                    packet_data = json.loads(line)

                    # Navigate through the nested structure to get the frame number
                    frame_number_str = packet_data['_source']['layers']['frame']['frame.number']
                    frame_number = int(frame_number_str)

                    # If the frame number exceeds the limit, stop processing
                    if frame_number > max_frame_number:
                        print(f"\nEncountered frame {frame_number} on line {line_num}, which is > {max_frame_number}.")
                        print("Stopping processing.")
                        break

                    # Write the original line to the output file
                    outfile.write(line)

                except json.JSONDecodeError:
                    print(f"Warning: Could not decode JSON on line {line_num}. Skipping.", file=sys.stderr)
                    continue
                except KeyError:
                    print(f"Warning: 'frame.number' not found in the expected path on line {line_num}. Skipping.", file=sys.stderr)
                    continue
                except ValueError:
                    print(f"Warning: Could not convert 'frame.number' to an integer on line {line_num}. Skipping.", file=sys.stderr)
                    continue

        print("\nProcessing complete.")
        print(f"Output successfully saved to {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The input file '{input_file_path}' was not found.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    # --- Configuration ---
    # Change these file paths to match your input and desired output files
    INPUT_FILENAME = "packets.json"
    OUTPUT_FILENAME = "packets_cut_after_10000.json"
    MAX_FRAME = 10000

    # --- Run the function ---
    filter_packets_by_frame_number(INPUT_FILENAME, OUTPUT_FILENAME, MAX_FRAME)