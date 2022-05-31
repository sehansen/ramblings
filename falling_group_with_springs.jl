using Plots;

gravity = true;
num_iters = 60;
timescale = 0.01;
spring_constant = 0.2;

objects_ys = 0.1 * [0, 1, 2, 3, 4];
masses = [1, 1, 1, 1, 1];
velocities = zeros(5);

a_history = zeros(num_iters, 5);
v_history = zeros(num_iters, 5);
y_history = zeros(num_iters, 5);

for iteration = 1:num_iters
    diffs = objects_ys[2:end] - objects_ys[1:end-1]
    print(diffs)
    print("\n")
    forces = zeros(5);
    for ix = 1:4
        if diffs[ix] < 0.11
            forces[ix] += spring_constant * (diffs[ix] - 0.11)/0.01;
            forces[ix+1] += -spring_constant * (diffs[ix] - 0.11)/0.01;
        end
    end

    if gravity
        accelerations = (forces .- 9.82) ./ masses;
    else
        accelerations = forces ./ masses;
    end

    a_history[iteration, :] = accelerations;
    v_history[iteration, :] = velocities;
    y_history[iteration, :] = objects_ys;

    global velocities += accelerations * timescale;

    global objects_ys += velocities * timescale;
end


display(plot(plot(1:num_iters, y_history), plot(1:num_iters, v_history), plot(1:num_iters, a_history), layout = (3, 1)));

readline();
