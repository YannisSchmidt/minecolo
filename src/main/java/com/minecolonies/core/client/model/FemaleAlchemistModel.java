// Made with Blockbench 3.5.1
// Exported for Minecraft version 1.15
// Paste this class into your mod and generate all required imports
package com.minecolonies.core.client.model;

import com.minecolonies.api.client.render.modeltype.CitizenModel;
import com.minecolonies.api.entity.citizen.AbstractEntityCitizen;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;
import net.minecraft.client.model.HumanoidModel;
import net.minecraft.world.entity.Pose;
import org.jetbrains.annotations.NotNull;

public class FemaleAlchemistModel extends CitizenModel<AbstractEntityCitizen>
{

    public FemaleAlchemistModel(final ModelPart part)
    {
        super(part);
        hat.visible = false;
    }

    public static LayerDefinition createMesh()
    {
        MeshDefinition meshdefinition = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition partDefinition = meshdefinition.getRoot();

        PartDefinition Head = partDefinition.addOrReplaceChild("head", CubeListBuilder.create()
          .texOffs(0, 0).addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F, new CubeDeformation(0.0F))
          .texOffs(32, 0).addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F, new CubeDeformation(0.5F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        PartDefinition HairExtension = Head.addOrReplaceChild("HairExtension", CubeListBuilder.create().texOffs(56, 0).addBox(-4.0F, 0.0F, 3.0F, 8.0F, 7.0F, 1.0F, new CubeDeformation(0.5F)), PartPose.offset(0.0F, 1.0F, 0.0F));

        PartDefinition Ponytail = Head.addOrReplaceChild("Ponytail", CubeListBuilder.create(), PartPose.offset(0.0F, 24.0F, 0.0F));

        PartDefinition ponyTailTip_r1 = Ponytail.addOrReplaceChild("ponyTailTip_r1", CubeListBuilder.create().texOffs(88, 55).addBox(0.0F, 0.0F, 0.0F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.1F)), PartPose.offsetAndRotation(-0.5F, -25.0F, 4.8F, 0.2231F, 0.0F, 0.0F));

        PartDefinition ponytailBase_r1 = Ponytail.addOrReplaceChild("ponytailBase_r1", CubeListBuilder.create().texOffs(86, 48).addBox(0.0F, 0.0F, 0.0F, 2.0F, 5.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-1.0F, -28.0F, 2.0F, 0.5577F, 0.0F, 0.0F));

        PartDefinition PointHat = Head.addOrReplaceChild("PointHat", CubeListBuilder.create()
          .texOffs(96, 0).addBox(-4.0F, -1.99F, -4.0F, 8.0F, 2.0F, 8.0F, new CubeDeformation(0.67F))
          .texOffs(76, 10).addBox(-8.0F, -0.4F, -5.0F, 16.0F, 1.0F, 10.0F, new CubeDeformation(0.0F))
          .texOffs(98, 21).addBox(-5.0F, -0.4F, -8.0F, 10.0F, 1.0F, 3.0F, new CubeDeformation(0.0F))
          .texOffs(93, 21).addBox(-7.0F, -0.4F, -7.0F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
          .texOffs(85, 21).addBox(5.0F, -0.4F, -7.0F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
          .texOffs(93, 25).addBox(-7.0F, -0.4F, 5.0F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
          .texOffs(85, 25).addBox(5.0F, -0.4F, 5.0F, 2.0F, 1.0F, 2.0F, new CubeDeformation(0.0F))
          .texOffs(98, 25).addBox(-5.0F, -0.4F, 5.0F, 10.0F, 1.0F, 3.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.0F, -6.2F, -0.1F, -1.0272F, 1.4692F, -1.0325F));

        PartDefinition top4_r1 = PointHat.addOrReplaceChild("top4_r1", CubeListBuilder.create().texOffs(84, 0).addBox(-0.3F, -9.5F, -2.4F, 2.0F, 3.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.0F, 0.1F, -0.4F, -0.5638F, -0.2158F, -0.1694F));

        PartDefinition top3_r1 = PointHat.addOrReplaceChild("top3_r1", CubeListBuilder.create().texOffs(88, 1).addBox(-2.5F, -7.5F, -1.8F, 4.0F, 3.0F, 4.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.0F, 0.1F, -0.4F, -0.3051F, -0.0885F, 0.0096F));

        PartDefinition top2_r1 = PointHat.addOrReplaceChild("top2_r1", CubeListBuilder.create().texOffs(58, 9).addBox(-3.5F, -4.9F, -3.8F, 7.0F, 3.0F, 7.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.0F, 0.1F, 0.0F, -0.1752F, -0.0859F, 0.0152F));

        PartDefinition glasses = Head.addOrReplaceChild("glasses", CubeListBuilder.create()
          .texOffs(54, 19).addBox(-5.5F, -3.6F, -1.3F, 7.0F, 7.0F, 1.0F, new CubeDeformation(-2.0F))
          .texOffs(54, 27).addBox(-1.5F, -3.6F, -1.3F, 7.0F, 7.0F, 1.0F, new CubeDeformation(-2.0F))
          .texOffs(70, 19).addBox(-1.0F, -0.6F, -2.55F, 2.0F, 1.0F, 1.0F, new CubeDeformation(-0.3F))
          .texOffs(70, 21).addBox(-4.8F, -0.9F, -2.89F, 2.0F, 2.0F, 5.0F, new CubeDeformation(-0.6F))
          .texOffs(65, 30).addBox(2.8F, -0.9F, -2.89F, 2.0F, 2.0F, 5.0F, new CubeDeformation(-0.6F)), PartPose.offsetAndRotation(0.0F, -3.9F, -2.1F, 0.0873F, 0.0F, 0.0F));

        PartDefinition Body = partDefinition.addOrReplaceChild("body", CubeListBuilder.create()
          .texOffs(16, 16).addBox(-4.0F, 0.0F, -2.0F, 8.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
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

        PartDefinition capeBody = Body.addOrReplaceChild("capeBody", CubeListBuilder.create()
          .texOffs(102, 36).addBox(-4.0F, -5.2F, -2.5F, 8.0F, 2.0F, 5.0F, new CubeDeformation(0.21F))
          .texOffs(108, 43).addBox(-5.0F, -3.0F, 2.7F, 10.0F, 18.0F, 0.0F, new CubeDeformation(0.0F)), PartPose.offset(0.0F, 5.0F, 0.0F));

        PartDefinition Potion1 = Body.addOrReplaceChild("Potion1", CubeListBuilder.create()
          .texOffs(81, 37).addBox(-1.4152F, 3.4965F, -1.4F, 5.0F, 6.0F, 5.0F, new CubeDeformation(-1.4F))
          .texOffs(91, 52).addBox(-0.9152F, 4.2965F, -0.9F, 4.0F, 5.0F, 4.0F, new CubeDeformation(-1.3F))
          .texOffs(96, 48).addBox(0.0848F, 3.6465F, 0.1F, 2.0F, 2.0F, 2.0F, new CubeDeformation(-0.5F))
          .texOffs(61, 39).addBox(-1.4152F, 4.5465F, -1.4F, 5.0F, 4.0F, 5.0F, new CubeDeformation(-1.3F)), PartPose.offset(1.3F, 4.78F, -4.2F));

        PartDefinition IngredientPouch = Body.addOrReplaceChild("IngredientPouch", CubeListBuilder.create()
          .texOffs(78, 35).addBox(-1.1333F, -0.9417F, -0.35F, 2.0F, 1.0F, 1.0F, new CubeDeformation(-0.1F))
          .texOffs(79, 33).addBox(-0.6333F, -1.4417F, -0.35F, 1.0F, 1.0F, 1.0F, new CubeDeformation(-0.25F))
          .texOffs(84, 33).addBox(-1.6333F, -0.2417F, -0.35F, 3.0F, 3.0F, 1.0F, new CubeDeformation(0.0F))
          .texOffs(86, 28).addBox(-1.6333F, -0.1417F, -1.45F, 3.0F, 3.0F, 2.0F, new CubeDeformation(-0.4F))
          .texOffs(97, 36).addBox(-1.3333F, -1.9417F, -0.65F, 4.0F, 4.0F, 1.0F, new CubeDeformation(-1.0F)), PartPose.offsetAndRotation(-2.0667F, 10.3417F, -2.65F, 0.0F, 0.0F, 0.0436F));

        PartDefinition top_r1 = IngredientPouch.addOrReplaceChild("top_r1", CubeListBuilder.create().texOffs(81, 31).addBox(-0.5F, -2.65F, -0.5F, 1.0F, 0.0F, 1.0F, new CubeDeformation(-0.1F)), PartPose.offsetAndRotation(-0.1333F, 1.3583F, 0.15F, 0.0F, -0.2618F, 0.0F));

        PartDefinition Right_Arm = partDefinition.addOrReplaceChild("right_arm", CubeListBuilder.create()
          .texOffs(40, 16).addBox(-2.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(40, 32).addBox(-2.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(-5.0F, 2.0F, 0.0F));

        PartDefinition capeShoulderRight = Right_Arm.addOrReplaceChild("capeShoulderRight", CubeListBuilder.create().texOffs(112, 29).addBox(-1.0F, -1.0F, -2.5F, 3.0F, 2.0F, 5.0F, new CubeDeformation(0.2F)), PartPose.offset(-1.1F, -1.2F, 0.0F));

        PartDefinition Left_Arm = partDefinition.addOrReplaceChild("left_arm", CubeListBuilder.create()
          .texOffs(32, 48).addBox(-1.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(48, 48).addBox(-1.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(5.0F, 2.0F, 0.0F));

        PartDefinition capeShoulderLeft = Left_Arm.addOrReplaceChild("capeShoulderLeft", CubeListBuilder.create().texOffs(96, 29).addBox(-2.0F, -1.0F, -2.5F, 3.0F, 2.0F, 5.0F, new CubeDeformation(0.2F)), PartPose.offset(1.1F, -1.2F, 0.0F));

        PartDefinition Right_Leg = partDefinition.addOrReplaceChild("right_leg", CubeListBuilder.create()
          .texOffs(0, 16).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(0, 32).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(-1.9F, 12.0F, 0.0F));

        PartDefinition Left_Leg = partDefinition.addOrReplaceChild("left_leg", CubeListBuilder.create()
          .texOffs(16, 48).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(0, 48).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(1.9F, 12.0F, 0.0F));

        return LayerDefinition.create(meshdefinition, 128, 64);
    }

    @Override
    public void setupAnim(@NotNull final AbstractEntityCitizen entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch)
    {
        super.setupAnim(entity, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);
        head.getChild("glasses").visible = isWorking(entity);
        head.getChild("PointHat").visible = entity.getPose() != Pose.SLEEPING && displayHat(entity);
        body.getChild("Potion1").visible = entity.getPose() != Pose.SLEEPING;
        body.getChild("IngredientPouch").visible = entity.getPose() != Pose.SLEEPING;
    }
}
