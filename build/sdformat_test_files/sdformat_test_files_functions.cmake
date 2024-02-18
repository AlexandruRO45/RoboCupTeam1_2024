# This file assumes sdformat_test_files_MODELS_DIR exists

function(sdformat_test_files_has_model arg model_name)
  set(known_model_names geometry_box;geometry_cylinder;geometry_heightmap;geometry_mesh_collada;geometry_mesh_obj;geometry_mesh_scaled;geometry_mesh_stl;geometry_plane;geometry_sphere;graph_chain;graph_chain_non_canonical_root;graph_four_bar;graph_loop;graph_tree;graph_tree_non_canonical_root;joint_ball;joint_continuous;joint_fixed;joint_gearbox;joint_prismatic;joint_prismatic_no_axis;joint_revolute;joint_revolute2;joint_revolute_axis;joint_revolute_axis_in_frame;joint_revolute_default_limits;joint_revolute_two_joints_two_links;joint_screw;joint_universal;link_inertia;link_light_point;link_multiple_collisions;link_multiple_visuals;link_sensor_imu;material_blinn_phong;material_dynamic_lights;model_two_models;model_zero_models;pose_chain;pose_collision;pose_collision_in_frame;pose_inertial;pose_inertial_in_frame;pose_joint;pose_joint_all;pose_joint_in_frame;pose_link;pose_link_all;pose_link_in_frame;pose_model;pose_visual;pose_visual_in_frame)
  foreach(known_model_name ${model_names})
    if("${model_name}" STREQUAL "${known_model_name")
      set("${arg}" TRUE PARENT_SCOPE)
      return()
    endif()
  endforeach()
  set("${arg}" "${model_name}-NOTFOUND}" PARENT_SCOPE)
endfunction()

# Get path to directory containing model.config for a model with the given name
function(sdformat_test_files_get_model_path arg model_name)
  sdformat_test_files_has_model("has_model" "${model_name}")
  if(NOT has_model)
    message(FATAL_ERROR "Unknown model ${model_name}")
  endif()

  set("${arg}" "${sdformat_test_files_MODELS_DIR}/${model_name}" PARENT_SCOPE)
endfunction()

# Get path to <model>.sdf for a model with the given name
function(sdformat_test_files_get_model_sdf arg model_name)
  sdformat_test_files_has_model("has_model" "${model_name}")
  if(NOT has_model)
    message(FATAL_ERROR "Unknown model ${model_name}")
  endif()

  set("${arg}" "${sdformat_test_files_MODELS_DIR}/${model_name}/${model_name}.sdf" PARENT_SCOPE)
endfunction()
