using ImageView, Images, Gtk.ShortNames, ColorTypes;

dims = 400

img = zeros(dims, dims)
rgbimg = Array{RGB, 2}(undef, dims, dims)

corners = rand(2, 2) * 100

for i in range(1, length=dims)
    for j in range(1, length=dims)
        img[i, j] += corners[1, 1] * (dims - i) * (dims - j) / (dims - 1) / (dims - 1)
        img[i, j] += corners[1, 2] * (dims - i) * (j-1) / (dims - 1) / (dims - 1)
        img[i, j] += corners[2, 1] * (i-1) * (dims - j) / (dims - 1) / (dims - 1)
        img[i, j] += corners[2, 2] * (i-1) * (j-1) / (dims - 1) / (dims - 1)
        if (rand() > i / dims)
            rgbimg[i, j] = RGB(0, img[i, j] / 100, 1)
        else
            rgbimg[i, j] = RGB(0, img[i, j] / 100, 0)
        end
    end
end

print(corners)

print("\n")

@assert(abs(corners[1, 1] - img[1, 1]) < 0.01, "Top left")
@assert(abs(corners[1, 2] - img[1, dims]) < 0.01, "Top right")
@assert(abs(corners[2, 1] - img[dims, 1]) < 0.01, "Bottom left")
@assert(abs(corners[2, 2] - img[dims, dims]) < 0.01, "Bottom right")


guidict = imshow(rgbimg); #, CLim(0, 100))

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
