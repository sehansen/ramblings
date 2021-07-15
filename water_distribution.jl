using ImageView, Images, Gtk.ShortNames;

img = zeros(100, 100)

corners = rand(2, 2) * 100

for i in range(1, length=100)
    for j in range(1, length=100)
        img[i, j] += corners[1, 1] * (100 - i) * (100 - j) / 99 / 99
        img[i, j] += corners[1, 2] * (100 - i) * (j-1) / 99 / 99
        img[i, j] += corners[2, 1] * (i-1) * (100 - j) / 99 / 99
        img[i, j] += corners[2, 2] * (i-1) * (j-1) / 99 / 99
    end
end

print(corners)

print("\n")

@assert(abs(corners[1, 1] - img[1, 1]) < 0.01, "Top left")
@assert(abs(corners[1, 2] - img[1, 100]) < 0.01, "Top right")
@assert(abs(corners[2, 1] - img[100, 1]) < 0.01, "Bottom left")
@assert(abs(corners[2, 2] - img[100, 100]) < 0.01, "Bottom right")

guidict = imshow(img, CLim(0, 100))

print(guidict["clim"])

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
