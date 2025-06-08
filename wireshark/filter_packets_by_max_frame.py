#!/usr/bin/env python3
import json
import sys

def filter_packets_by_frame_number_advanced(input_file_path, output_file_path, max_frame_number=10000):
    """
    Reads multi-line JSON objects from an input file, and writes them to an
    output file until a frame number greater than the max_frame_number is found.
    This version is more robust and handles "pretty-printed" JSON.
    """
    print(f"Starting advanced processing...")
    print(f"Input file: {input_file_path}")
    print(f"Output file: {output_file_path}")
    print(f"Will cut everything after frame number {max_frame_number}.")

    object_buffer = ""
    found_start = False

    try:
        with open(input_file_path, 'r') as infile, open(output_file_path, 'w') as outfile:
            for line_num, line in enumerate(infile, 1):
                # Ignore lines until we find the start of an object
                if not found_start and line.strip().startswith('{'):
                    found_start = True

                if not found_start:
                    continue
                
                # Add the current line to our buffer
                object_buffer += line

                # Try to parse the buffer. If it's not a complete object, just continue.
                try:
                    # Successfully parsed a complete JSON object
                    packet_data = json.loads(object_buffer)

                    # --- Processing Logic ---
                    frame_number_str = packet_data['_source']['layers']['frame']['frame.number']
                    frame_number = int(frame_number_str)

                    if frame_number > max_frame_number:
                        print(f"\nEncountered frame {frame_number}, which is > {max_frame_number}.")
                        print("Stopping processing.")
                        break # Exit the loop and stop reading the file
                    
                    # Write the buffer (which is one full object) to the output
                    # and then reset the buffer for the next object.
                    outfile.write(object_buffer)
                    object_buffer = ""
                    found_start = False

                except json.JSONDecodeError:
                    # This is expected if the object is spread across multiple lines.
                    # We just continue to the next line to add more data to the buffer.
                    continue
                except (KeyError, ValueError) as e:
                    print(f"Warning: Could not process a valid JSON object ending on line {line_num}. It might be missing keys or have wrong values. Error: {e}. Skipping object.", file=sys.stderr)
                    # Reset buffer and move on
                    object_buffer = ""
                    found_start = False
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
    INPUT_FILENAME = "input.json"
    OUTPUT_FILENAME = "output.json"
    MAX_FRAME = 10000

    # --- Run the function ---
    filter_packets_by_frame_number_advanced(INPUT_FILENAME, OUTPUT_FILENAME, MAX_FRAME)