use strict;
use warnings;
use Path::Tiny;
use FindBin;

use lib "$FindBin::Bin";
use lib "$FindBin::Bin/2023/Solutions/perl";
use AOCUtils;


my @input_list = AOCUtils::get_day_input(1);

my $res = 0;
# loop through each row, get first and last number, join them, and add them to the result
#  if only one number, join it with itself
foreach my $row (@input_list) {
    my @digits = $row =~ /\d/g;
    my $value = @digits == 1 ? $digits[0] . $digits[0] : $digits[0] . $digits[-1];
    $res += $value;
}

print "Part 1: $res\n";

$res = 0;
# loop through each row, get first and last number, join them, and add them to the result
#  if only one number, join it with itself
#   now even literal numbers count 'one', 'two', 'three', etc, these hase to be 
#   converted to digits
foreach my $row (@input_list) {
    # using lookahead regex to get overlapping matches without consuming characters
    my @matches = $row =~ /(?=(\d|one|two|three|four|five|six|seven|eight|nine))/g;
        foreach my $match (@matches) {
        $match =~ s/one/1/g;
        $match =~ s/two/2/g;
        $match =~ s/three/3/g;
        $match =~ s/four/4/g;
        $match =~ s/five/5/g;
        $match =~ s/six/6/g;
        $match =~ s/seven/7/g;
        $match =~ s/eight/8/g;
        $match =~ s/nine/9/g;
    }
    my $value = @matches == 1 ? $matches[0] . $matches[0] : $matches[0] . $matches[-1];
    $res += $value;
}

print "Part 2: $res\n";