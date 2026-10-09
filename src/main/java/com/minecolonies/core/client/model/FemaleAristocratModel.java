// Made with Blockbench 4.0.0-beta.0
// Exported for Minecraft version 1.17 with Mojang mappings
// Paste this class into your mod and generate all required imports
package com.minecolonies.core.client.model;

import com.minecolonies.api.client.render.modeltype.CitizenModel;
import com.minecolonies.api.entity.citizen.AbstractEntityCitizen;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;
import net.minecraft.world.entity.Pose;
import org.jetbrains.annotations.NotNull;

public class FemaleAristocratModel extends CitizenModel<AbstractEntityCitizen>
{
    private final ModelPart umbrellaArm;

    public FemaleAristocratModel(final ModelPart part)
    {
        super(part);
        this.umbrellaArm = part.getChild("FoldedLeftArm");
        hat.visible = false;
    }

    public static LayerDefinition createMesh()
    {
		MeshDefinition meshdefinition = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
		PartDefinition partdefinition = meshdefinition.getRoot();

        PartDefinition bipedHead = partdefinition.addOrReplaceChild("head", CubeListBuilder.create().texOffs(0, 0).addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F, new CubeDeformation(0.0F))
          .texOffs(32, 0).addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F, new CubeDeformation(0.5F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        PartDefinition nobleHair = bipedHead.addOrReplaceChild("nobleHair", CubeListBuilder.create().texOffs(64, 0).addBox(-4.0F, 0.0F, 3.0F, 8.0F, 9.0F, 1.0F, new CubeDeformation(0.5F)), PartPose.offset(0.0F, 1.0F, 0.0F));

        PartDefinition hairdetailfront = bipedHead.addOrReplaceChild("hairdetailfront", CubeListBuilder.create().texOffs(68, 10).addBox(-4.5F, 8.0F, -4.0F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F))
          .texOffs(64, 10).mirror().addBox(3.4F, 8.0F, -4.0F, 1.0F, 9.0F, 1.0F, new CubeDeformation(0.0F)).mirror(false), PartPose.offset(0.0F, -7.5F, 0.7F));

        PartDefinition aristocratHair = bipedHead.addOrReplaceChild("aristocratHair", CubeListBuilder.create().texOffs(82, 2).addBox(-2.0F, -6.0F, -3.0F, 4.0F, 2.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(82, 8).addBox(-1.0F, -4.0F, -2.0F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
          .texOffs(72, 11).addBox(-3.0F, -3.0F, -4.0F, 6.0F, 3.0F, 6.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, -8.0F, 2.0F));

        PartDefinition hairback2_r1 = aristocratHair.addOrReplaceChild("hairback2_r1", CubeListBuilder.create().texOffs(90, 28).addBox(-1.0F, -1.0F, 0.8F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
          .texOffs(90, 21).addBox(-2.0F, -2.0F, -2.2F, 4.0F, 4.0F, 3.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.1F, 3.1F, 3.9F, 0.1309F, 0.0F, 0.0F));

        PartDefinition FancyHat = bipedHead.addOrReplaceChild("FancyHat", CubeListBuilder.create().texOffs(84, 33).addBox(-7.1F, -0.3625F, -5.0F, 12.0F, 1.0F, 10.0F, new CubeDeformation(0.0F))
          .texOffs(104, 44).addBox(-5.1F, -0.3625F, -7.0F, 10.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
          .texOffs(124, 50).addBox(-6.1F, -0.3625F, -6.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
          .texOffs(106, 50).addBox(4.9F, -2.3625F, -5.0F, 1.0F, 3.0F, 10.0F, new CubeDeformation(0.0F))
          .texOffs(124, 54).addBox(4.9F, -1.3625F, 5.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
          .texOffs(124, 57).addBox(4.9F, -1.3625F, -6.0F, 1.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
          .texOffs(124, 52).addBox(-6.1F, -0.3625F, 5.0F, 1.0F, 1.0F, 1.0F, new CubeDeformation(0.0F))
          .texOffs(104, 47).addBox(-5.1F, -0.3625F, 5.0F, 10.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
          .texOffs(96, 23).addBox(-4.1F, -1.9525F, -4.0F, 8.0F, 2.0F, 8.0F, new CubeDeformation(0.6F)), PartPose.offsetAndRotation(0.1F, -7.1375F, 0.0F, 0.0873F, -0.0175F, -0.0436F));

        PartDefinition feather2_r1 = FancyHat.addOrReplaceChild("feather2_r1", CubeListBuilder.create().texOffs(88, 44).addBox(-0.7F, -5.9F, -0.8F, 0.0F, 7.0F, 9.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-4.4F, -1.1125F, 1.318F, -0.1858F, -0.528F, -0.0543F));

        PartDefinition bipedBody = partdefinition.addOrReplaceChild("body", CubeListBuilder.create().texOffs(16, 16).addBox(-4.0F, 0.0F, -2.0F, 8.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(16, 32).addBox(-4.0F, 0.0F, -2.0F, 8.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        PartDefinition breast = bipedBody.addOrReplaceChild("breast", CubeListBuilder.create()
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

        PartDefinition SkirtTop = bipedBody.addOrReplaceChild("SkirtTop", CubeListBuilder.create(), PartPose.offset(0.0F, 9.0F, 0.0F));

        PartDefinition p1 = SkirtTop.addOrReplaceChild("p1", CubeListBuilder.create().texOffs(0, 64).addBox(-2.0F, -3.5F, -2.0F, 4.0F, 7.0F, 4.0F, new CubeDeformation(-0.2F)), PartPose.offsetAndRotation(-2.9156F, 3.541F, -1.9156F, -0.1745F, 0.7854F, 0.0F));

        PartDefinition p2 = SkirtTop.addOrReplaceChild("p2", CubeListBuilder.create().texOffs(16, 64).addBox(-2.0F, -3.5F, -2.0F, 4.0F, 7.0F, 4.0F, new CubeDeformation(-0.2F)), PartPose.offsetAndRotation(-2.8158F, 3.5642F, 2.0156F, -0.1745F, 2.3562F, 0.0F));

        PartDefinition p3 = SkirtTop.addOrReplaceChild("p3", CubeListBuilder.create().texOffs(32, 64).addBox(-2.0F, -3.5F, -2.0F, 4.0F, 7.0F, 4.0F, new CubeDeformation(-0.2F)), PartPose.offsetAndRotation(2.9339F, 3.5848F, 1.9341F, -0.1745F, -2.3562F, 0.0F));

        PartDefinition p4 = SkirtTop.addOrReplaceChild("p4", CubeListBuilder.create().texOffs(48, 64).addBox(-2.0F, -3.5F, -2.0F, 4.0F, 7.0F, 4.0F, new CubeDeformation(-0.2F)), PartPose.offsetAndRotation(2.8763F, 3.5775F, -1.9762F, -0.1745F, -0.7854F, 0.0F));

        PartDefinition p5 = SkirtTop.addOrReplaceChild("p5", CubeListBuilder.create().texOffs(64, 64).addBox(-2.0F, -3.5F, -2.0F, 4.0F, 7.0F, 4.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(3.66F, 3.5943F, 0.0001F, -0.1745F, -1.5708F, 0.0F));

        PartDefinition p6 = SkirtTop.addOrReplaceChild("p6", CubeListBuilder.create().texOffs(80, 64).addBox(-2.0F, -3.5F, -2.0F, 4.0F, 7.0F, 4.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-3.6539F, 3.5224F, -0.0001F, -0.1745F, 1.5708F, 0.0F));

        PartDefinition p7 = SkirtTop.addOrReplaceChild("p7", CubeListBuilder.create().texOffs(96, 64).addBox(-2.0F, -3.5F, -2.0F, 4.0F, 7.0F, 4.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.1F, 3.653F, 2.7943F, 0.2443F, 0.0F, 0.0F));

        PartDefinition p8 = SkirtTop.addOrReplaceChild("p8", CubeListBuilder.create().texOffs(112, 64).addBox(-2.0F, -3.5F, -2.0F, 4.0F, 7.0F, 4.0F, new CubeDeformation(-0.2F)), PartPose.offsetAndRotation(-0.1F, 3.5232F, -3.3134F, -0.2967F, 0.0F, 0.0F));

        PartDefinition SkirtMiddle = bipedBody.addOrReplaceChild("SkirtMiddle", CubeListBuilder.create(), PartPose.offset(0.0F, 16.0F, 0.0F));

        PartDefinition Middle2_r1 = SkirtMiddle.addOrReplaceChild("Middle2_r1", CubeListBuilder.create().texOffs(48, 75).addBox(-6.0F, -2.0F, -6.0F, 12.0F, 4.0F, 12.0F, new CubeDeformation(0.01F)), PartPose.offsetAndRotation(0.0F, 0.0F, 0.0F, 0.0F, -1.5708F, 0.0F));

        PartDefinition Middle1_r1 = SkirtMiddle.addOrReplaceChild("Middle1_r1", CubeListBuilder.create().texOffs(0, 75).addBox(-6.0F, -2.0F, -6.0F, 12.0F, 4.0F, 12.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.0F, 0.0F, 0.0F, 0.0F, -0.7854F, 0.0F));

        PartDefinition SkirtBottom = bipedBody.addOrReplaceChild("SkirtBottom", CubeListBuilder.create(), PartPose.offset(0.0F, 20.0F, 0.0F));

        PartDefinition bottom2_r1 = SkirtBottom.addOrReplaceChild("bottom2_r1", CubeListBuilder.create().texOffs(52, 91).addBox(-6.5F, -6.5F, -6.5F, 13.0F, 6.0F, 13.0F, new CubeDeformation(0.01F)), PartPose.offsetAndRotation(0.0F, 4.0F, 0.0F, 0.0F, -1.5708F, 0.0F));

        PartDefinition bottom1_r1 = SkirtBottom.addOrReplaceChild("bottom1_r1", CubeListBuilder.create().texOffs(0, 91).addBox(-6.5F, -6.5F, -6.5F, 13.0F, 6.0F, 13.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.0F, 4.0F, 0.0F, 0.0F, -0.7854F, 0.0F));

        PartDefinition bipedRightArm = partdefinition.addOrReplaceChild("right_arm", CubeListBuilder.create().texOffs(40, 16).addBox(-2.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(40, 32).addBox(-2.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offsetAndRotation(-5.0F, 2.0F, 0.0F, 0.0F, 0.0F, 0.0873F));

        PartDefinition bipedLeftArm = partdefinition.addOrReplaceChild("left_arm", CubeListBuilder.create().texOffs(32, 48).addBox(-1.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(48, 48).addBox(-1.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offsetAndRotation(5.0F, 2.0F, 0.0F, 0.0F, 0.0F, -0.0873F));

        PartDefinition FoldedLeftArm = partdefinition.addOrReplaceChild("FoldedLeftArm", CubeListBuilder.create(), PartPose.offset(5.0F, 2.0F, 0.0F));

        PartDefinition shoulderArm = FoldedLeftArm.addOrReplaceChild("shoulderArm", CubeListBuilder.create().texOffs(56, 20).addBox(-1.01F, -2.01F, -2.0F, 3.0F, 6.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(56, 30).addBox(-1.011F, -2.0F, -2.01F, 3.0F, 6.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        PartDefinition foreArm = FoldedLeftArm.addOrReplaceChild("foreArm", CubeListBuilder.create().texOffs(72, 20).addBox(9.99F, -1.5F, -2.5F, 3.0F, 7.0F, 4.0F, new CubeDeformation(0.01F))
          .texOffs(72, 31).addBox(9.99F, -1.45F, -2.5F, 3.0F, 7.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offsetAndRotation(-11.0F, 4.5F, 0.5F, -1.5708F, 0.0F, 0.0F));

        PartDefinition umbrella = FoldedLeftArm.addOrReplaceChild("umbrella", CubeListBuilder.create().texOffs(86, 20).addBox(-0.5F, -20.5F, -0.5F, 1.0F, 21.0F, 1.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.5F, 3.5F, -6.0F, -0.6097F, 0.04F, 0.0572F));

        PartDefinition umbrella_r1 = umbrella.addOrReplaceChild("umbrella_r1", CubeListBuilder.create().texOffs(92, 11).addBox(-4.5F, -0.5F, -4.5F, 9.0F, 1.0F, 9.0F, new CubeDeformation(-0.01F)), PartPose.offsetAndRotation(0.0F, -18.8075F, 0.0138F, -0.1841F, 0.7769F, -0.1298F));

        PartDefinition umbrella_r2 = umbrella.addOrReplaceChild("umbrella_r2", CubeListBuilder.create().texOffs(92, 0).addBox(-4.5F, -0.5F, -4.5F, 9.0F, 1.0F, 9.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.0F, -18.8075F, 0.0138F, -0.1309F, 0.0F, 0.0F));

        PartDefinition bipedRightLeg = partdefinition.addOrReplaceChild("right_leg", CubeListBuilder.create().texOffs(0, 16).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(0, 32).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(-1.9F, 12.0F, 0.0F));

        PartDefinition bipedLeftLeg = partdefinition.addOrReplaceChild("left_leg", CubeListBuilder.create().texOffs(16, 48).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(0, 48).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(1.9F, 12.0F, 0.0F));

        return LayerDefinition.create(meshdefinition, 128, 128);
	}

    @Override
    public void setupAnim(@NotNull final AbstractEntityCitizen entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch)
    {
        super.setupAnim(entity, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);
        body.getChild("SkirtMiddle").visible = entity.getPose() != Pose.SLEEPING;
        body.getChild("SkirtBottom").visible = entity.getPose() != Pose.SLEEPING;
        body.getChild("SkirtTop").visible = entity.getPose() != Pose.SLEEPING;
        head.getChild("FancyHat").visible = entity.getPose() != Pose.SLEEPING && displayHat(entity);
        umbrellaArm.visible = entity.getPose() != Pose.SLEEPING;
    }

    @Override
    public void renderToBuffer(
      final @NotNull PoseStack matrixStack,
      final @NotNull VertexConsumer buffer,
      final int packedLight,
      final int packedOverlay,
      final int color)
    {
        super.renderToBuffer(matrixStack, buffer, packedLight, packedOverlay, color);
        umbrellaArm.render(matrixStack, buffer, packedLight, packedOverlay, color);
    }
}
