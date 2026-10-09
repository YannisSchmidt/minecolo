// Made with Blockbench 4.1.5
// Exported for Minecraft version 1.15 - 1.16 with Mojang mappings
// Paste this class into your mod and generate all required imports
package com.minecolonies.core.client.model;

import com.minecolonies.api.client.render.modeltype.CitizenModel;
import com.minecolonies.api.entity.citizen.AbstractEntityCitizen;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;
import org.jetbrains.annotations.NotNull;

public class FemaleEnchanterModel extends CitizenModel<AbstractEntityCitizen>
{
	public FemaleEnchanterModel(ModelPart root)
	{
        super(root);
		hat.visible = false;
	}

    public static LayerDefinition createMesh()
    {
        MeshDefinition meshdefinition = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition partdefinition = meshdefinition.getRoot();

        PartDefinition Head = partdefinition.addOrReplaceChild("head", CubeListBuilder.create().texOffs(0, 0).addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F, new CubeDeformation(0.0F))
          .texOffs(32, 0).addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F, new CubeDeformation(0.5F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        PartDefinition HairExtension = Head.addOrReplaceChild("HairExtension", CubeListBuilder.create().texOffs(56, 0).addBox(-4.0F, 0.0F, 3.0F, 8.0F, 7.0F, 1.0F, new CubeDeformation(0.5F)), PartPose.offset(0.0F, 1.0F, 0.0F));

        PartDefinition Ponytail = Head.addOrReplaceChild("Ponytail", CubeListBuilder.create(), PartPose.offset(0.0F, 24.0F, 0.0F));

        PartDefinition ponyTailTip_r1 = Ponytail.addOrReplaceChild("ponyTailTip_r1", CubeListBuilder.create().texOffs(88, 55).mirror().addBox(0.0F, 0.0F, 0.0F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.1F)).mirror(false), PartPose.offsetAndRotation(-0.5F, -25.0F, 4.8F, 0.2231F, 0.0F, 0.0F));

        PartDefinition ponytailBase_r1 = Ponytail.addOrReplaceChild("ponytailBase_r1", CubeListBuilder.create().texOffs(86, 48).mirror().addBox(0.0F, 0.0F, 0.0F, 2.0F, 5.0F, 2.0F, new CubeDeformation(0.0F)).mirror(false), PartPose.offsetAndRotation(-1.0F, -28.0F, 2.0F, 0.5577F, 0.0F, 0.0F));

        PartDefinition glasses = Head.addOrReplaceChild("glasses", CubeListBuilder.create().texOffs(64, 8).addBox(-5.5F, -3.6F, -1.3F, 7.0F, 7.0F, 1.0F, new CubeDeformation(-2.0F))
          .texOffs(64, 16).addBox(-1.5F, -3.6F, -1.3F, 7.0F, 7.0F, 1.0F, new CubeDeformation(-2.0F))
          .texOffs(80, 8).addBox(-1.0F, -0.6F, -2.55F, 2.0F, 1.0F, 1.0F, new CubeDeformation(-0.3F))
          .texOffs(75, 19).addBox(-4.8F, -0.9F, -2.89F, 2.0F, 2.0F, 5.0F, new CubeDeformation(-0.6F))
          .texOffs(75, 26).addBox(2.8F, -0.9F, -2.89F, 2.0F, 2.0F, 5.0F, new CubeDeformation(-0.6F)), PartPose.offsetAndRotation(0.0F, -3.7F, -2.1F, 0.0873F, 0.0F, 0.0F));

        PartDefinition Body = partdefinition.addOrReplaceChild("body", CubeListBuilder.create().texOffs(16, 16).addBox(-4.0F, 0.0F, -2.0F, 8.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(16, 32).addBox(-4.0F, 0.0F, -2.0F, 8.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        PartDefinition breast = Body.addOrReplaceChild("breast", CubeListBuilder.create()
          .texOffs(64, 49).addBox(-1.348F, 0.554F, -6.586F, 1.798F, 1.2F, 3.21F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.55F, 0.554F, -6.586F, 1.798F, 1.2F, 3.21F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.243F, 0.554F, -7.398F, 2.668F, 1.2F, 0.952F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.575F, 0.554F, -7.398F, 2.668F, 1.2F, 0.952F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.733F, 0.554F, -8.558F, 3.133F, 1.2F, 1.3F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.6F, 0.554F, -8.558F, 3.133F, 1.2F, 1.3F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.642F, 0.554F, -9.719F, 3.017F, 1.2F, 1.301F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.625F, 0.554F, -9.719F, 3.017F, 1.2F, 1.301F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.028F, 0.554F, -10.705F, 2.378F, 1.2F, 1.126F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.65F, 0.554F, -10.705F, 2.378F, 1.2F, 1.126F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-0.951F, 0.554F, -11.459F, 1.276F, 1.2F, 0.894F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.675F, 0.554F, -11.459F, 1.276F, 1.2F, 0.894F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.381F, 1.674F, -7.086F, 2.831F, 1.2F, 3.71F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.55F, 1.674F, -7.086F, 2.831F, 1.2F, 3.71F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.776F, 1.674F, -8.365F, 4.201F, 1.2F, 1.419F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.575F, 1.674F, -8.365F, 4.201F, 1.2F, 1.419F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.532F, 1.674F, -10.191F, 4.932F, 1.2F, 1.966F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.6F, 1.674F, -10.191F, 4.932F, 1.2F, 1.966F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.374F, 1.674F, -12.018F, 4.749F, 1.2F, 1.967F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.625F, 1.674F, -12.018F, 4.749F, 1.2F, 1.967F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.395F, 1.674F, -13.57F, 3.745F, 1.2F, 1.692F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.65F, 1.674F, -13.57F, 3.745F, 1.2F, 1.692F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-1.684F, 1.674F, -14.758F, 2.009F, 1.2F, 1.328F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.675F, 1.674F, -14.758F, 2.009F, 1.2F, 1.328F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.65F, 2.794F, -7.216F, 3.1F, 1.2F, 3.84F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.55F, 2.794F, -7.216F, 3.1F, 1.2F, 3.84F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.175F, 2.794F, -8.616F, 4.6F, 1.2F, 1.54F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.575F, 2.794F, -8.616F, 4.6F, 1.2F, 1.54F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-5.0F, 2.794F, -10.616F, 5.4F, 1.2F, 2.14F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.6F, 2.794F, -10.616F, 5.4F, 1.2F, 2.14F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.825F, 2.794F, -12.616F, 5.2F, 1.2F, 2.14F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.625F, 2.794F, -12.616F, 5.2F, 1.2F, 2.14F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.75F, 2.794F, -14.316F, 4.1F, 1.2F, 1.84F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.65F, 2.794F, -14.316F, 4.1F, 1.2F, 1.84F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-1.875F, 2.794F, -15.616F, 2.2F, 1.2F, 1.44F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.675F, 2.794F, -15.616F, 2.2F, 1.2F, 1.44F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.381F, 3.914F, -7.086F, 2.831F, 1.2F, 3.71F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.55F, 3.914F, -7.086F, 2.831F, 1.2F, 3.71F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.776F, 3.914F, -8.365F, 4.201F, 1.2F, 1.419F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.575F, 3.914F, -8.365F, 4.201F, 1.2F, 1.419F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.532F, 3.914F, -10.191F, 4.932F, 1.2F, 1.966F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.6F, 3.914F, -10.191F, 4.932F, 1.2F, 1.966F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-4.374F, 3.914F, -12.018F, 4.749F, 1.2F, 1.967F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.625F, 3.914F, -12.018F, 4.749F, 1.2F, 1.967F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.395F, 3.914F, -13.57F, 3.745F, 1.2F, 1.692F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.65F, 3.914F, -13.57F, 3.745F, 1.2F, 1.692F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-1.684F, 3.914F, -14.758F, 2.009F, 1.2F, 1.328F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.675F, 3.914F, -14.758F, 2.009F, 1.2F, 1.328F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-1.348F, 5.034F, -6.586F, 1.798F, 1.2F, 3.21F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.55F, 5.034F, -6.586F, 1.798F, 1.2F, 3.21F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.243F, 5.034F, -7.398F, 2.668F, 1.2F, 0.952F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.575F, 5.034F, -7.398F, 2.668F, 1.2F, 0.952F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.733F, 5.034F, -8.558F, 3.133F, 1.2F, 1.3F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.6F, 5.034F, -8.558F, 3.133F, 1.2F, 1.3F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.642F, 5.034F, -9.719F, 3.017F, 1.2F, 1.301F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.625F, 5.034F, -9.719F, 3.017F, 1.2F, 1.301F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.028F, 5.034F, -10.705F, 2.378F, 1.2F, 1.126F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.65F, 5.034F, -10.705F, 2.378F, 1.2F, 1.126F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-0.951F, 5.034F, -11.459F, 1.276F, 1.2F, 0.894F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.675F, 5.034F, -11.459F, 1.276F, 1.2F, 0.894F, BREAST_DEFORMATION),
          PartPose.offsetAndRotation(-1.0F, 3.0F, 4.0F, -0.14F, 0.0F, 0.0F));

        PartDefinition capeBody = Body.addOrReplaceChild("capeBody", CubeListBuilder.create().texOffs(102, 36).addBox(-4.0F, -5.2F, -2.5F, 8.0F, 2.0F, 5.0F, new CubeDeformation(0.21F))
          .texOffs(108, 43).addBox(-5.0F, -3.0F, 2.7F, 10.0F, 18.0F, 0.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, 5.0F, 0.0F));

        PartDefinition bag = Body.addOrReplaceChild("bag", CubeListBuilder.create(), PartPose.offset(0.0F, -0.1F, -0.3F));

        PartDefinition book2_r1 = bag.addOrReplaceChild("book2_r1", CubeListBuilder.create().texOffs(86, 4).mirror().addBox(-1.0F, 1.4F, -2.0F, 2.0F, 4.0F, 6.0F, new CubeDeformation(0.0F)).mirror(false)
          .texOffs(96, 8).mirror().addBox(-0.8F, -2.0F, -3.0F, 2.0F, 4.0F, 6.0F, new CubeDeformation(0.0F)).mirror(false), PartPose.offsetAndRotation(-5.8F, 9.5722F, 1.6111F, -1.6138F, 0.0076F, 0.1744F));

        PartDefinition strapback_r1 = bag.addOrReplaceChild("strapback_r1", CubeListBuilder.create().texOffs(122, 14).addBox(-0.5F, -14.3F, 0.0F, 1.0F, 15.0F, 0.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-5.5665F, 9.9968F, 4.2551F, 0.0913F, 0.0015F, 0.7592F));

        PartDefinition strapfrontb_r1 = bag.addOrReplaceChild("strapfrontb_r1", CubeListBuilder.create().texOffs(123, 14).addBox(-0.5F, -1.8F, 0.3F, 1.0F, 5.0F, 0.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(4.4558F, -0.5558F, 1.1519F, -1.5708F, 0.0F, 0.7854F));

        PartDefinition strapfrontb_r2 = bag.addOrReplaceChild("strapfrontb_r2", CubeListBuilder.create().texOffs(123, 19).addBox(-0.5F, -2.5F, 0.5F, 1.0F, 6.0F, 0.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(2.6008F, 1.2992F, -3.0977F, -0.2269F, 0.0F, 0.7854F));

        PartDefinition strapfronta_r1 = bag.addOrReplaceChild("strapfronta_r1", CubeListBuilder.create().texOffs(126, 14).addBox(-0.5F, -8.0F, 0.0F, 1.0F, 9.0F, 0.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-5.5F, 9.4F, -4.1F, -0.0873F, 0.0F, 0.7854F));

        PartDefinition bag_r1 = bag.addOrReplaceChild("bag_r1", CubeListBuilder.create().texOffs(106, 0).addBox(-1.9F, -3.0F, -4.0F, 3.0F, 6.0F, 8.0F, new CubeDeformation(0.03F)), PartPose.offsetAndRotation(-5.5F, 12.0F, 0.0F, 0.0F, 0.0F, 0.1222F));

        PartDefinition Right_Arm = partdefinition.addOrReplaceChild("right_arm", CubeListBuilder.create().texOffs(40, 16).addBox(-2.5F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(40, 32).addBox(-2.5F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offsetAndRotation(-5.0F, 2.0F, 0.0F, 0.0F, 0.0F, 0.3491F));

        PartDefinition capeShoulderRight = Right_Arm.addOrReplaceChild("capeShoulderRight", CubeListBuilder.create().texOffs(112, 29).addBox(-1.4F, -1.0F, -2.5F, 3.0F, 2.0F, 5.0F, new CubeDeformation(0.2F)), PartPose.offset(-1.1F, -1.2F, 0.0F));

        PartDefinition Left_Arm = partdefinition.addOrReplaceChild("left_arm", CubeListBuilder.create().texOffs(32, 48).addBox(-1.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(48, 48).addBox(-1.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(5.0F, 2.0F, 0.0F));

        PartDefinition capeShoulderLeft = Left_Arm.addOrReplaceChild("capeShoulderLeft", CubeListBuilder.create().texOffs(96, 29).addBox(-2.0F, -1.0F, -2.5F, 3.0F, 2.0F, 5.0F, new CubeDeformation(0.2F)), PartPose.offset(1.1F, -1.2F, 0.0F));

        PartDefinition Right_Leg = partdefinition.addOrReplaceChild("right_leg", CubeListBuilder.create().texOffs(0, 16).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(0, 32).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(-1.9F, 12.0F, 0.0F));

        PartDefinition Left_Leg = partdefinition.addOrReplaceChild("left_leg", CubeListBuilder.create().texOffs(16, 48).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(0, 48).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(1.9F, 12.0F, 0.0F));

        return LayerDefinition.create(meshdefinition, 128, 64);
    }

    @Override
    public void setupAnim(@NotNull final AbstractEntityCitizen entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch)
    {
        super.setupAnim(entity, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);
        body.getChild("bag").visible = isWorking(entity);
    }
}
