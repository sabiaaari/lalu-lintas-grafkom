#version 330 core

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform vec3 cam_pos;
uniform vec3 u_color;
uniform vec3 u_emissive;

in vec3 frag_pos;
in vec3 normal;

out vec4 fragColor;

void main() {
    vec3 N = normalize(normal);
    vec3 L = normalize(light.position - frag_pos);
    vec3 V = normalize(cam_pos - frag_pos);
    vec3 H = normalize(L + V);

    float diff = max(dot(N, L), 0.0);
    float spec = pow(max(dot(N, H), 0.0), 64.0) * step(0.0, diff);

    vec3 ambient = light.Ia * u_color;
    vec3 diffuse = light.Id * diff * u_color;
    vec3 specular = light.Is * spec;
    vec3 final_color = ambient + diffuse + specular + u_emissive;

    fragColor = vec4(final_color, 1.0);
}
