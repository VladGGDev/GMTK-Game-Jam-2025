import engine, engine.collider


def solve_circle_collision(a: engine.collider.CircleCollider, b: engine.collider.CircleCollider, unmovable_tags: set[str] = set[str]()) -> None:
    # Check if they are the same collider
    if a is b:
        return
    dist = a.position.distance_to(b.position) - a.radius - b.radius
    # No collision
    if dist > 0:
        return
    rel = b.position - a.position
    # Colliders perfectly overlap
    if rel.magnitude_squared() == 0:
        rel.y = -1
    # Move colliders if they are movable
    move = rel.normalize() * -dist / 2
    if a.tag not in unmovable_tags:
        a.position -= move
    if b.tag not in unmovable_tags:
        b.position += move

def solve_all_circle_collisions(unmovable_tags: set[str] = set[str]()) -> None:
    for coll in engine.collider.all_colliders:
        if not isinstance(coll, engine.collider.CircleCollider):
            continue
        for coll2 in engine.collider.all_colliders:
            if isinstance(coll2, engine.collider.CircleCollider):
                solve_circle_collision(coll, coll2, unmovable_tags)