extern "C" {
#include <png.h>

#include "wsq.h"
}

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include <string>

int debug;

static int write_grey_8bit_png(FILE *fl, void *image, int width, int height)
{
	unsigned char *pixels = static_cast<unsigned char *>(image);
	png_structp png;
	png_infop info;
	int row;

	png = png_create_write_struct(PNG_LIBPNG_VER_STRING,
		NULL, NULL, NULL);
	if (!png)
		return -__LINE__;

	info = png_create_info_struct(png);
	if (!info)
		return -__LINE__;

	if (setjmp(png_jmpbuf(png))) {
		png_destroy_write_struct(&png, &info);
		return -__LINE__;
	}

	png_init_io(png, fl);

	png_set_IHDR(png, info, width, height,
		8, PNG_COLOR_TYPE_GRAY, PNG_INTERLACE_NONE,
		PNG_COMPRESSION_TYPE_BASE, PNG_FILTER_TYPE_BASE);

	png_write_info(png, info);

	for (row = 0; row < height; row++)
		png_write_row(png, pixels + (width * row));

	png_write_end(png, NULL);

	png_destroy_write_struct(&png, &info);

	return 0;
}

static int read_grey_8bit_png(FILE *fl, void **image, int *width, int *height)
{
	unsigned char sig[8];
	png_structp png;
	png_infop info;
	png_uint_32 w, h;
	int bit_depth, color_type;
	int interlace_method, compression_method, filter_method;
	png_bytep *rows;
	int y;

	fread(sig, 1, 8, fl);
	if (!png_check_sig(sig, 8))
		return -__LINE__;

	png = png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);
	if (!png)
		return -__LINE__;

	info = png_create_info_struct(png);
	if (!info) {
		png_destroy_read_struct(&png, NULL, NULL);
		return -__LINE__;
	}

	png_init_io(png, fl);
	png_set_sig_bytes(png, 8);
	png_read_info(png, info);

	png_get_IHDR(png, info, &w, &h, &bit_depth, &color_type,
		&interlace_method, &compression_method, &filter_method);
	if (bit_depth != 8 || color_type != PNG_COLOR_TYPE_GRAY ||
		interlace_method != PNG_INTERLACE_NONE ||
		compression_method != PNG_COMPRESSION_TYPE_BASE ||
		filter_method != PNG_FILTER_TYPE_BASE) {
		png_destroy_read_struct(&png, NULL, NULL);
		return -__LINE__;
	}
	*width = w;
	*height = h;

	if (setjmp(png_jmpbuf(png))) {
		png_destroy_read_struct(&png, NULL, NULL);
		return -__LINE__;
	}

	rows = static_cast<png_bytep *>(malloc(sizeof(png_bytep) * h));
	if (!rows) {
		png_destroy_read_struct(&png, NULL, NULL);
		return -__LINE__;
	}
	for (y = 0; y < h; y++)
		rows[y] = static_cast<png_bytep>(malloc(png_get_rowbytes(png, info)));

	png_read_image(png, rows);

	png_destroy_read_struct(&png, NULL, NULL);

	*image = malloc(w * h);
	for (y = 0; y < h; y++)
		memcpy(((char *)(*image)) + (w * y), rows[y], w);

	for (y = 0; y < h; y++)
		free(rows[y]);
	free(rows);

	return 0;
}

static int wsq_to_png(char const* inputFile, char const* outputFile)
{
	FILE *in = NULL;
	FILE *out = NULL;
	int err;
	int width, height, depth, ppi, lossy;
	unsigned char *image;

	in = fopen(inputFile, "rb");
	if (!in) {
		perror(inputFile);
		return 1;
	}

	out = fopen(outputFile, "wb");
	if (!out) {
		perror(outputFile);
		return 1;
	}

	panda();

	err = wsq_decode_file(&image, &width, &height, &depth, &ppi,
		&lossy, in);
	if (err) {
		fprintf(stderr, "Failed to compress image! (%d)\n", err);
		return 1;
	}
	if (depth != 8)
		fprintf(stderr, "Warning: expected 8-bit image, got %d...\n",
			depth);

	err = write_grey_8bit_png(out, image, width, height);
	if (err) {
		fprintf(stderr, "Failed to read PNG image! (%d)\n", err);
		return 1;
	}

	if (in != stdin)
		fclose(in);

	if (out != stdout)
		fclose(out);

	free(image);

	return 0;
}

static int png_to_wsq(char const* inputFile, char const* outputFile)
{
	FILE *in = NULL;
	FILE *out = NULL;
	int err;
	int width, height;
	float bitrate = 0.75;
	unsigned char *image;
	unsigned char *wsq;
	int size;

	in = fopen(inputFile, "rb");
	if (!in) {
		perror(inputFile);
		return 1;
	}

	out = fopen(outputFile, "wb");
	if (!out) {
		perror(outputFile);
		return 1;
	}

	err = read_grey_8bit_png(in, (void **)&image, &width, &height);
	if (err) {
		fprintf(stderr, "Failed to read PNG image! (%d)\n", err);
		return 1;
	}

	err = wsq_encode_mem(&wsq, &size, bitrate,
		image, width, height, 8, -1, NULL);
	if (err) {
		fprintf(stderr, "Failed to compress image! (%d)\n", err);
		return 1;
	}
	if (fwrite(wsq, size, 1, out) != 1) {
		perror("fwrite");
		return -1;
	}

	if (in != stdin)
		fclose(in);

	if (out != stdout)
		fclose(out);

	free(image);

	return 0;
}

#include <boost/python.hpp>
BOOST_PYTHON_MODULE(wsq)
{
	using namespace boost::python;
	def("wsq_to_png", wsq_to_png);
	def("png_to_wsq", png_to_wsq);
}
