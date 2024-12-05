use strict;
use warnings;
use Path::Tiny;

use FindBin;

use lib "$FindBin::Bin";
use lib "$FindBin::Bin/2023/Solutions/perl";
use AOCUtils;


my @input_list = AOCUtils::get_day_input(2);

# init the CARDS for part 1, red=12, green=13 and blue=14
my %part_1_cards = (
    "red" => 12,
    "green" => 13,
    "blue" => 14
);

my ($part_1_res, $part_2_res) = (0, 0);

# loop through each row

foreach my $row (@input_list) {
    #print "New row!\n";
    # each row will have the format: 
    # Game X: {{hand},..}; {.,.};.;.
    # use the regex "Game (\d+):" to get the game captured group
    my %part_2_cards = (
        "red" => 0,
        "green" => 0,
        "blue" => 0
    );

    my $game_n = 0;
    if ($row =~ /^Game (\d+):/) {
        $game_n = $1;
    }
    
    while ($row =~ /((\d+) (red|green|blue))/g){
        # $1 hold something like "12 red",
        # $2 holds the number, and $3 the color
        if ($2 > $part_1_cards{$3}) {
            # to skip this row and avoid adding it to the result
            # set game_n to 0
            $game_n = 0;
            # cannot use last because part 2 needs all the hands
        }
        # if part_2_cards[color] < value, set it to value
        if ($2 > $part_2_cards{$3}) {
            $part_2_cards{$3} = $2;
        }
    }
    $part_1_res += $game_n;

    # part_2_res += product of the 3 cards values
    $part_2_res += $part_2_cards{"red"} * $part_2_cards{"green"} * $part_2_cards{"blue"};
}

print "Part 1: $part_1_res\n";
print "Part 2: $part_2_res\n";