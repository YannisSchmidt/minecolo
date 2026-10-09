// Made with Blockbench 4.0.0-beta.0
// Exported for Minecraft version 1.17 with Mojang mappings
// Paste this class into your mod and generate all required imports
package com.minecolonies.core.client.model;

import com.minecolonies.api.client.render.modeltype.CitizenModel;
import com.minecolonies.api.entity.citizen.AbstractEntityCitizen;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;
import net.minecraft.world.entity.Pose;
import org.jetbrains.annotations.NotNull;

import static com.minecolonies.core.entity.ai.workers.service.EntityAIWorkDeliveryman.RENDER_META_BACKPACK;

public class FemaleCourierModel extends CitizenModel<AbstractEntityCitizen>
{
    public FemaleCourierModel(ModelPart root)
    {
        super(root);
        hat.visible = false;
    }

    public static LayerDefinition createMesh()
    {
        MeshDefinition meshdefinition = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition partdefinition = meshdefinition.getRoot();

        PartDefinition bipedHead = partdefinition.addOrReplaceChild("head", CubeListBuilder.create()
          .texOffs(0, 0).addBox(-4.0F, -7.0F, -3.6148F, 8.0F, 8.0F, 8.0F, new CubeDeformation(0.0F))
          .texOffs(32, 0).addBox(-4.0F, -7.0F, -3.6148F, 8.0F, 8.0F, 8.0F, new CubeDeformation(0.5F)), PartPose.offsetAndRotation(0.0F, -0.2F, -2.1F, 0.0873F, 0.0F, 0.0F));

        PartDefinition Ponytail = bipedHead.addOrReplaceChild("Ponytail", CubeListBuilder.create(), PartPose.offsetAndRotation(0.0F, 1.3F, 4.9F, 0.48F, 0.0F, 0.0F));

        PartDefinition ponyTailTip_r1 = Ponytail.addOrReplaceChild("ponyTailTip_r1", CubeListBuilder.create().texOffs(88, 55).addBox(0.0F, 1.0F, -0.1F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.1F)), PartPose.offsetAndRotation(-0.5F, -1.502F, 3.1709F, 0.2231F, 0.0F, 0.0F));

        PartDefinition ponytailBase_r1 = Ponytail.addOrReplaceChild("ponytailBase_r1", CubeListBuilder.create().texOffs(86, 48).addBox(0.0F, 1.0F, -0.3F, 2.0F, 5.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-1.0F, -4.502F, 0.3709F, 0.5577F, 0.0F, 0.0F));

        PartDefinition bipedBody = partdefinition.addOrReplaceChild("body", CubeListBuilder.create().texOffs(16, 16).addBox(-4.0F, -11.35F, -2.0F, 8.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(16, 32).addBox(-4.0F, -11.35F, -2.0F, 8.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offsetAndRotation(0.0F, 12.0F, 0.0F, 0.1745F, 0.0F, 0.0F));

        PartDefinition backpack = bipedBody.addOrReplaceChild("backpack", CubeListBuilder.create().texOffs(100, 50).addBox(-4.0F, -1.7F, 0.0F, 8.0F, 8.0F, 6.0F, new CubeDeformation(0.3F)), PartPose.offset(0.0F, -6.9F, 2.3F));

        PartDefinition lid_r1 = backpack.addOrReplaceChild("lid_r1", CubeListBuilder.create().texOffs(100, 42).addBox(-4.0F, -1.2F, -0.5F, 8.0F, 2.0F, 6.0F, new CubeDeformation(0.4F)), PartPose.offsetAndRotation(0.0F, -2.1F, 0.6F, 0.0436F, 0.0F, 0.0F));

        PartDefinition breast = bipedBody.addOrReplaceChild("breast", CubeListBuilder.create()
          .texOffs(64, 49).addBox(-1.348F, 0.954F, -6.586F, 1.798F, 1.2F, 3.21F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.55F, 0.954F, -6.586F, 1.798F, 1.2F, 3.21F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.243F, 0.954F, -7.398F, 2.668F, 1.2F, 0.952F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.575F, 0.954F, -7.398F, 2.668F, 1.2F, 0.952F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.733F, 0.954F, -8.558F, 3.133F, 1.2F, 1.3F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.6F, 0.954F, -8.558F, 3.133F, 1.2F, 1.3F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.642F, 0.954F, -9.719F, 3.017F, 1.2F, 1.301F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.625F, 0.954F, -9.719F, 3.017F, 1.2F, 1.301F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.028F, 0.954F, -10.705F, 2.378F, 1.2F, 1.126F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.65F, 0.954F, -10.705F, 2.378F, 1.2F, 1.126F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-0.951F, 0.954F, -11.459F, 1.276F, 1.2F, 0.894F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.675F, 0.954F, -11.459F, 1.276F, 1.2F, 0.894F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.381F, 2.074F, -7.086F, 2.831F, 1.2F, 3.71F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.55F, 2.074F, -7.086F, 2.831F, 1.2F, 3.71F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.776F, 2.074F, -8.365F, 4.201F, 1.2F, 1.419F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.575F, 2.074F, -8.365F, 4.201F, 1.2F, 1.419F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.532F, 2.074F, -10.191F, 4.932F, 1.2F, 1.966F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.6F, 2.074F, -10.191F, 4.932F, 1.2F, 1.966F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.374F, 2.074F, -12.018F, 4.749F, 1.2F, 1.967F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.625F, 2.074F, -12.018F, 4.749F, 1.2F, 1.967F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.395F, 2.074F, -13.57F, 3.745F, 1.2F, 1.692F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.65F, 2.074F, -13.57F, 3.745F, 1.2F, 1.692F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-1.684F, 2.074F, -14.758F, 2.009F, 1.2F, 1.328F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.675F, 2.074F, -14.758F, 2.009F, 1.2F, 1.328F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.65F, 3.194F, -7.216F, 3.1F, 1.2F, 3.84F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.55F, 3.194F, -7.216F, 3.1F, 1.2F, 3.84F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.175F, 3.194F, -8.616F, 4.6F, 1.2F, 1.54F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.575F, 3.194F, -8.616F, 4.6F, 1.2F, 1.54F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-5.0F, 3.194F, -10.616F, 5.4F, 1.2F, 2.14F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.6F, 3.194F, -10.616F, 5.4F, 1.2F, 2.14F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.825F, 3.194F, -12.616F, 5.2F, 1.2F, 2.14F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.625F, 3.194F, -12.616F, 5.2F, 1.2F, 2.14F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.75F, 3.194F, -14.316F, 4.1F, 1.2F, 1.84F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.65F, 3.194F, -14.316F, 4.1F, 1.2F, 1.84F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-1.875F, 3.194F, -15.616F, 2.2F, 1.2F, 1.44F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.675F, 3.194F, -15.616F, 2.2F, 1.2F, 1.44F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.381F, 4.314F, -7.086F, 2.831F, 1.2F, 3.71F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.55F, 4.314F, -7.086F, 2.831F, 1.2F, 3.71F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.776F, 4.314F, -8.365F, 4.201F, 1.2F, 1.419F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.575F, 4.314F, -8.365F, 4.201F, 1.2F, 1.419F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.532F, 4.314F, -10.191F, 4.932F, 1.2F, 1.966F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.6F, 4.314F, -10.191F, 4.932F, 1.2F, 1.966F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.374F, 4.314F, -12.018F, 4.749F, 1.2F, 1.967F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.625F, 4.314F, -12.018F, 4.749F, 1.2F, 1.967F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.395F, 4.314F, -13.57F, 3.745F, 1.2F, 1.692F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.65F, 4.314F, -13.57F, 3.745F, 1.2F, 1.692F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-1.684F, 4.314F, -14.758F, 2.009F, 1.2F, 1.328F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.675F, 4.314F, -14.758F, 2.009F, 1.2F, 1.328F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-1.348F, 5.434F, -6.586F, 1.798F, 1.2F, 3.21F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.55F, 5.434F, -6.586F, 1.798F, 1.2F, 3.21F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.243F, 5.434F, -7.398F, 2.668F, 1.2F, 0.952F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.575F, 5.434F, -7.398F, 2.668F, 1.2F, 0.952F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.733F, 5.434F, -8.558F, 3.133F, 1.2F, 1.3F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.6F, 5.434F, -8.558F, 3.133F, 1.2F, 1.3F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.642F, 5.434F, -9.719F, 3.017F, 1.2F, 1.301F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.625F, 5.434F, -9.719F, 3.017F, 1.2F, 1.301F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.028F, 5.434F, -10.705F, 2.378F, 1.2F, 1.126F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.65F, 5.434F, -10.705F, 2.378F, 1.2F, 1.126F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-0.951F, 5.434F, -11.459F, 1.276F, 1.2F, 0.894F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.675F, 5.434F, -11.459F, 1.276F, 1.2F, 0.894F, BREAST_DEFORMATION),
          PartPose.offsetAndRotation(-1.0F, -9.0F, 4.0F, -0.14F, 0.0F, 0.0F));

        PartDefinition bipedRightArm = partdefinition.addOrReplaceChild("right_arm", CubeListBuilder.create().texOffs(40, 16).addBox(-2.0F, -1.8F, -2.3F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(40, 32).addBox(-2.0F, -1.8F, -2.3F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(-5.0F, 2.5F, -1.6F));

        PartDefinition bipedLeftArm = partdefinition.addOrReplaceChild("left_arm", CubeListBuilder.create().texOffs(32, 48).addBox(-1.0F, -1.8F, -2.3F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(48, 48).addBox(-1.0F, -1.8F, -2.3F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(5.0F, 2.5F, -1.6F));

        PartDefinition bipedRightLeg = partdefinition.addOrReplaceChild("right_leg", CubeListBuilder.create().texOffs(0, 16).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(0, 32).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(-1.9F, 12.0F, 0.0F));

        PartDefinition bipedLeftLeg = partdefinition.addOrReplaceChild("left_leg", CubeListBuilder.create().texOffs(16, 48).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(0, 48).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(1.9F, 12.0F, 0.0F));

        return LayerDefinition.create(meshdefinition, 128, 64);
    }

    @Override
    public float getActualRotation(@NotNull final AbstractEntityCitizen entity)
    {
        return entity.getPose() == Pose.SLEEPING || !entity.getRenderMetadata().contains(RENDER_META_BACKPACK) ? 0 : 0.1745F;
    }

    @Override
    public void setupAnim(@NotNull final AbstractEntityCitizen entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch)
    {
        super.setupAnim(entity, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);
        body.y += 12;

        final boolean showBackPack = entity.getPose() != Pose.SLEEPING && entity.getRenderMetadata().contains(RENDER_META_BACKPACK);
        head.z = showBackPack ? -2.1f : 0;
        head.getChild("Ponytail").xRot = showBackPack ? 0.48f : 0.1f;
        head.getChild("Ponytail").z = showBackPack ? 4.9f : 3f;
        body.getChild("backpack").visible = showBackPack;
        leftArm.y = showBackPack ? 2f : 2.5f;
        rightArm.y = showBackPack ? 2f : 2.5f;
    }
}
