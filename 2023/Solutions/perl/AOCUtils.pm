package AOCUtils;

use strict;
use warnings;
use File::Spec;

sub get_day_input {
    my ($day, $is_test) = @_;
    $is_test //= 0;
    my $file_path = get_file_path($day, $is_test);

    open my $fh, '<', $file_path or die "Could not open file '$file_path' $!";
    my @lines = <$fh>;
    close $fh;

    chomp @lines;
    return @lines;
}

sub get_file_path {
    my ($day, $is_test) = @_;
    $is_test //= 0;
    my $file_name = sprintf("C:/syncthing/shared_code_tests/adventOfCode/2023/day_%02d/%sinput.txt", $day, $is_test ? "test_" : "");
    return File::Spec->rel2abs($file_name);
}

1;