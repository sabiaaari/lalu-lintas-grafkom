#version 330 core

struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform vec3 cam_pos;
uniform sampler2D u_texture;
uniform vec3 u_emissive;
uniform float u_use_texture;
uniform vec2 u_uv_offset;
uniform vec2 u_uv_scale;

in vec3 frag_pos;
in vec3 normal;
in vec2 uv;

out vec4 fragColor;

void main() {
    vec3 N = normalize(normal);
    vec3 L = normalize(light.position - frag_pos);
    vec3 V = normalize(cam_pos - frag_pos);
    vec3 R = reflect(-L, N);

    float diff = max(dot(N, L), 0.0);
    float spec = pow(max(dot(V, R), 0.0), 32.0) * step(0.0, diff);

    vec3 base_color;
    if (u_use_texture > 0.5) {
        vec2 corrected_uv = uv * u_uv_scale + u_uv_offset;
        base_color = texture(u_texture, corrected_uv).rgb;
    } else {
        base_color = vec3(0.5); // Default color if no texture
    }

    vec3 ambient = light.Ia * base_color;
    vec3 diffuse = light.Id * diff * base_color;
    vec3 specular = light.Is * spec;
    
    vec3 final_color = ambient + diffuse + specular + u_emissive;

    fragColor = vec4(final_color, 1.0);
}
