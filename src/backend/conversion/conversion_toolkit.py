import subprocess
import markdown
from backend.gpt_utils.gpt_analysis_env import GptAnalysisEnv


class FileConverterToolkit:
    def convert_html(self, input_html: str, output_file: str, output_format: str):
        """
        Convert HTML content to a specified file format using pandoc.
        :param input_html: Path to the input HTML file.
        :param output_file: Path to the output file.
        :param output_format: Desired output format (e.g., 'PDF', 'PPTX', 'DOCX').
        """
        try:
            if output_format.upper() == 'PDF':
                subprocess.run(
                    ['pandoc', input_html, '-o', output_file, '--pdf-engine=wkhtmltopdf'],
                    check=True
                )
            else:
                subprocess.run(
                    ['pandoc', input_html, '-o', output_file, '-f', 'html'],
                    check=True
                )

            print(f"Conversion to {output_format} successful! Saved as {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error during conversion to {output_format}: {e}")

    def convert_markdown(self, markdown_text: str, output_file: str, output_format: str):
        """
        Convert Markdown content to a specified file format using pandoc.
        :param markdown_text: Markdown text content.
        :param output_file: Path to the output file.
        :param output_format: Desired output format (e.g., 'PDF', 'PPTX', 'DOCX').
        """
        try:
            # Convert Markdown text to HTML first
            html_content = markdown.markdown(markdown_text)
            temp_html_file = 'temp.html'

            with open(temp_html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Convert the temporary HTML to the desired format
            self.convert_html(temp_html_file, output_file, output_format)
        except Exception as e:
            print(f"Error during Markdown conversion to {output_format}: {e}")


# Example usage
if __name__ == "__main__":
    # Create the toolkit instance
    converter = FileConverterToolkit()

    # Example: Converting Markdown to different formats
    analysis_env = GptAnalysisEnv()
    markdown_text = analysis_env.summarize_conversation()

    converter.convert_markdown(markdown_text, 'output.pptx', 'PPTX')
    converter.convert_markdown(markdown_text, 'output.docx', 'DOCX')
    converter.convert_markdown(markdown_text, 'output.pdf', 'PDF')

    # Example: Converting an HTML file to different formats
    html_file = "/home/user/example.html"
    converter.convert_html(html_file, 'output.docx', 'DOCX')
    converter.convert_html(html_file, 'output.pdf', 'PDF')
