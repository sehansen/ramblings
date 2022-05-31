using ImageView, Images, Gtk.ShortNames, ColorTypes;
using LinearAlgebra;


river = 4;
ocean = 1;



playing_field = 20 * ones(100, 100);

citypos = (30, 45);

playing_field[1:100, 46:55] .= river;
playing_field[41:60, 1:100] .= ocean;

distance = Inf * ones(100, 100);
distance[citypos[1], citypos[2]] = 0;

pot_distance_up = Inf * ones(100, 100);
pot_distance_down = Inf * ones(100, 100);
pot_distance_left = Inf * ones(100, 100);
pot_distance_right = Inf * ones(100, 100);

first = true;
iteration_no = 0;

last_distance = zeros(100, 100);

while first || maximum(distance) == Inf && iteration_no < 500
    global first = false
    global iteration_no += 1;
    pot_distance_up[1:99, 1:100] = distance[2:100, 1:100] + playing_field[1:99, 1:100];
    pot_distance_down[2:100, 1:100] = distance[1:99, 1:100] + playing_field[2:100, 1:100];
    pot_distance_left[1:100, 1:99] = distance[1:100, 2:100] + playing_field[1:100, 1:99];
    pot_distance_right[1:100, 2:100] = distance[1:100, 1:99] + playing_field[1:100, 2:100];

    global last_distance = distance;
    global distance = min.(pot_distance_up, pot_distance_down, pot_distance_left, pot_distance_right, distance);
end


guidict = imshow((1 .+ distance).^0.6);

print("\n")
print("\n")
print("\n")
print("\n")

if (!isinteractive())
    c = Condition()

    win = guidict["gui"]["window"]

    signal_connect(win, :destroy) do widget
        notify(c)
    end

    wait(c)
end
