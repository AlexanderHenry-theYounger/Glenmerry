#!/usr/bin/perl -w

#
# Small file to generate a header file with the current revision.
# Used in the savegames to help track which revision was used when compiling.
#

use strict;
use warnings;

use File::Slurp;


my $file = "DLLSources/autogenerated/AutoGitVersion.h";

# read the repository revision hash from STDIN
my $version = <>;
# remove the trailing newline
$version =~ s/\R//g;

if ($version eq "READ")
{
	$version = readFile();
	rename "WeThePeople-temp.zip", "WeThePeople-" . $version . ".zip" if -e "WeThePeople-temp.zip"
}

my $output = "";

# generate the file content
$output .= "#ifndef AUTO_GIT_VERSION_H\n";
$output .= "#define AUTO_GIT_VERSION_H\n";
$output .= "const char* szGitVersion = \"" . $version . "\";\n";
$output .= "#endif\n";

# read the existing file
if (-e $file)
{
	my $file_content = read_file($file);
	# quit if the two files are identical
	# updating anyway will for an unneeded recompilation
	exit if $file_content eq $output;
}

# save the file
open (my $output_file, "> " . $file) or die "Can't open file " . $file . "\n" . $!;
print $output_file $output;
close $output_file;


# read the version from the changelog.txt
# fairly primitive. It uses the string from the first line starting with "Version "
sub readFile
{
	my $filename = '../changelog.txt';
	open(my $fh, '<:encoding(UTF-8)', $filename)
	  or die "Could not open file '$filename' $!";

	while (my $row = <$fh>) {
	  chomp $row;
	  next unless substr($row, 0, 8) eq "Version ";
	  $row =~ s/\R//g;
	  return substr($row, 8);
	}
}