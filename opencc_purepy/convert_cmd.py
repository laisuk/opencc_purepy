import io
import sys
import os
from opencc_purepy import OpenCC
from .office_doc_helper import OFFICE_FORMATS, convert_office_doc # Must be available

def main(args):
    if getattr(args, "office", False):
        input_file = args.input
        output_file = args.output
        office_format = args.format
        auto_ext = getattr(args, "auto_ext", False)
        config = args.config
        punct = args.punct
        keep_font = getattr(args, "keep_font", False)

        if not input_file and not output_file:
            print("❌ Input and output files are missing.", file=sys.stderr)
            return 1
        if not input_file:
            print("❌ Input file is missing.", file=sys.stderr)
            return 1

        if not output_file:
            input_name = os.path.splitext(os.path.basename(input_file))[0]
            input_dir = os.path.dirname(input_file) or os.getcwd()
            ext = f".{office_format}" if auto_ext and office_format and office_format in OFFICE_FORMATS else os.path.splitext(input_file)[1]
            output_file = os.path.join(input_dir, f"{input_name}_converted{ext}")
            print(f"ℹ️ Output file not specified. Using: {output_file}", file=sys.stderr)

        if not office_format:
            file_ext = os.path.splitext(input_file)[1].lower()
            if file_ext[1:] not in OFFICE_FORMATS:
                print(f"❌ Invalid Office file extension: {file_ext}", file=sys.stderr)
                print("   Valid extensions: .docx | .xlsx | .pptx | .odt | .ods | .odp | .epub", file=sys.stderr)
                return 1
            office_format = file_ext[1:]

        if auto_ext and output_file and not os.path.splitext(output_file)[1] and office_format in OFFICE_FORMATS:
            output_file += f".{office_format}"
            print(f"ℹ️ Auto-extension applied: {output_file}", file=sys.stderr)

        try:
            success, message =convert_office_doc(
                input_file,
                output_file,
                office_format,
                OpenCC(config),
                punct,
                keep_font,
            )
            if success:
                print(f"{message}\n📁 Output saved to: {os.path.abspath(output_file)}", file=sys.stderr)
                return 0
            else:
                print(f"❌ Conversion failed: {message}", file=sys.stderr)
                return 1
        except Exception as ex:
            print(f"❌ Error during Office document conversion: {str(ex)}", file=sys.stderr)
            return 1

    # Plain text conversion fallback
    if args.config is None:
        print("Please specify conversion.", file=sys.stderr)
        return 1

    opencc = OpenCC(args.config)

    if args.input is None and sys.stdin.isatty():
        print("Input text to convert, <Ctrl+Z>/<Ctrl+D> to submit:", file=sys.stderr)

    with io.open(args.input if args.input else 0, encoding=args.in_enc) as f:
        input_str = f.read()

    output_str = opencc.convert(input_str, args.punct)

    with io.open(args.output if args.output else 1, 'w', encoding=args.out_enc) as f:
        f.write(output_str)

    in_from = args.input if args.input else "<stdin>"
    out_to = args.output if args.output else "stdout"
    if sys.stderr.isatty():
        print(f"Conversion completed ({args.config}): {in_from} -> {out_to}", file=sys.stderr)

    return 0
