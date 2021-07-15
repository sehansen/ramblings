using Random

struct Node
    id::UInt64
end

struct ComparisonLine
    x_id::UInt64
    y_id::UInt64
    x_votes::UInt32
    y_votes::UInt32
end

struct ComparisonDB
    outcomes::Vector{ComparisonLine}
end

function lt_simple(db::ComparisonDB, x::Node, y::Node)::Bool
    if x.id > y.id
        return gt_simple(db, y, x)
    else
        print(x.id)
        print(y.id)
        for line in db.outcomes
            print(line)
            print("\n")
            if line.x_id == x.id && line.y_id == y.id
                if line.x_votes < line.y_votes
                    return true
                else
                    return false
                end
            end
        end
        exit(1)
    end
end

function gt_simple(db::ComparisonDB, x::Node, y::Node)::Bool
    if x.id > y.id
        return lt_simple(db, y, x)
    else
        for line in db.outcomes
            if line.x_id == x.id && line.y_id == y.id
                if line.x_votes > line.y_votes
                    return true
                else
                    return false
                end
            end
        end
    end
end

function get_all_nodes_greater_than(db, x)
    outs = []
    for line in db.outcomes
        if line.x_id == x.id
            if line.x_votes < line.y_votes
                push!(outs, Node(line.y_id))
            end
        elseif line.y_id == x.id
            if line.y_votes < line.x_votes
                push!(outs, Node(line.x_id))
            end
        end
    end
    return outs
end

function intersection(list_a, list_b)
    outs = []
    for x in list_a
        for y in list_b
            if x == y
                push!(outs, x)
                break
            end
        end
    end
    return outs
end

function minimal_elements(db, elements_in)::Vector{Node}
    mins = []
    for x in elements_in
        minimal = true
        for y in elements_in
            if x.id == y.id
                continue
            elseif lt_simple(db, y, x)
                minimal = false
                break
            end
        end
        if minimal
            push!(mins, x)
        end
    end
    return mins
end

function get_upper_bounds(db, node_a, node_b)::Vector{Node}
    gt_a = get_all_nodes_greater_than(db, node_a)
    gt_b = get_all_nodes_greater_than(db, node_b)
    gt_ab = intersection(gt_a, gt_b)
    return minimal_elements(db, gt_ab)
end

function get_supremum(db, node_a, node_b)::Union{Node,Nothing}
    ub = get_upper_bounds(db, node_a, node_b)
    if length(ub) == 1
        return ub[1]
    else
        return nothing
    end
end;

function get_infimum(node_a, node_b)::Union{Node,Nothing}
end;

test_db = ComparisonDB([ComparisonLine(0, 1, 2, 3),
                        ComparisonLine(0, 2, 4, 5),
                        ComparisonLine(0, 3, 6, 5),
                        ComparisonLine(1, 2, 6, 7),
                        ComparisonLine(1, 3, 8, 7),
                        ComparisonLine(2, 3, 9, 1)])
test_x = Node(0)
test_y = Node(1)


print(get_supremum(test_db, test_x, test_y))
