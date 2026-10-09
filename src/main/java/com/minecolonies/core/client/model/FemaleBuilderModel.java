// Made with Blockbench 3.5.1
// Exported for Minecraft version 1.15
// Paste this class into your mod and generate all required imports
//
// Modified (minecolo fork):
//  - the flat cap ("Cap") was replaced by a yellow construction hard hat ("HardHat")
//  - a leather tool belt ("toolBelt") and a rolled-up blueprint ("blueprintRoll")
//    were added to the work gear ("toolbag" group, only visible while working)
//  - the hair bun is lowered to the nape while the hard hat is worn
//  The new parts use texture space that was previously unused (or used by the old cap),
//  see tools/female_builder/paint_female_builder_textures.py for the texture side.
package com.minecolonies.core.client.model;

import com.minecolonies.api.client.render.modeltype.CitizenModel;
import com.minecolonies.api.entity.citizen.AbstractEntityCitizen;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.*;
import net.minecraft.client.model.HumanoidModel;
import org.jetbrains.annotations.NotNull;

public class FemaleBuilderModel extends CitizenModel<AbstractEntityCitizen>
{
    /**
     * Name of the hard hat group (child of the head).
     */
    private static final String HARD_HAT = "HardHat";

    /**
     * Name of the hair bun part (child of the head).
     */
    private static final String HAIR_BUN = "hairback2_r1";

    /**
     * Default (Blockbench) y pivot of the hair bun, mid height of the back of the head.
     */
    private static final float HAIR_BUN_DEFAULT_Y = -4.9F;

    /**
     * Y pivot of the hair bun while the hard hat is worn: the hair is tied lower,
     * on the nape, so the bun comes out below the back edge of the hard hat shell.
     */
    private static final float HAIR_BUN_LOW_Y = -2.7F;

    public FemaleBuilderModel(final ModelPart part)
    {
        super(part);
        hat.visible = false;
    }

    public static LayerDefinition createMesh()
    {
        MeshDefinition meshdefinition = HumanoidModel.createMesh(CubeDeformation.NONE, 0.0F);
        PartDefinition partdefinition = meshdefinition.getRoot();

        PartDefinition bipedHead = partdefinition.addOrReplaceChild("head", CubeListBuilder.create().texOffs(0, 0).addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F, new CubeDeformation(0.0F))
          .texOffs(32, 0).addBox(-4.0F, -8.0F, -4.0F, 8.0F, 8.0F, 8.0F, new CubeDeformation(0.5F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        PartDefinition hairback2_r1 = bipedHead.addOrReplaceChild(HAIR_BUN, CubeListBuilder.create().texOffs(74, 7).addBox(-1.0F, -1.0F, 1.1F, 2.0F, 2.0F, 1.0F, new CubeDeformation(0.0F))
          .texOffs(74, 0).addBox(-2.0F, -2.0F, -1.9F, 4.0F, 4.0F, 3.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.1F, HAIR_BUN_DEFAULT_Y, 5.9F, 0.1309F, 0.0F, 0.0F));

        PartDefinition HairExtension = bipedHead.addOrReplaceChild("HairExtension", CubeListBuilder.create().texOffs(56, 0).addBox(-4.0F, 0.0F, 3.0F, 8.0F, 7.0F, 1.0F, new CubeDeformation(0.5F)), PartPose.offset(0.0F, 1.0F, 0.0F));

        PartDefinition Ponytail = bipedHead.addOrReplaceChild("Ponytail", CubeListBuilder.create(), PartPose.offset(0.0F, 24.0F, 0.0F));

        PartDefinition ponyTailTip_r1 = Ponytail.addOrReplaceChild("ponyTailTip_r1", CubeListBuilder.create().texOffs(88, 55).mirror().addBox(0.0F, 0.0F, 0.0F, 1.0F, 5.0F, 1.0F, new CubeDeformation(0.1F)).mirror(false), PartPose.offsetAndRotation(-0.5F, -25.0F, 4.8F, 0.2231F, 0.0F, 0.0F));

        PartDefinition ponytailBase_r1 = Ponytail.addOrReplaceChild("ponytailBase_r1", CubeListBuilder.create().texOffs(86, 48).mirror().addBox(0.0F, 0.0F, 0.0F, 2.0F, 5.0F, 2.0F, new CubeDeformation(0.0F)).mirror(false), PartPose.offsetAndRotation(-1.0F, -28.0F, 2.0F, 0.5577F, 0.0F, 0.0F));

        // ---- Construction hard hat (replaces the old flat cap). Pivot = top centre of the head. ----
        PartDefinition HardHat = bipedHead.addOrReplaceChild(HARD_HAT, CubeListBuilder.create(), PartPose.offset(0.0F, -8.0F, 0.0F));

        // main shell wrapping the top of the head (0.6 inflation: 0.1 outside the hair layer)
        PartDefinition shell = HardHat.addOrReplaceChild("shell", CubeListBuilder.create().texOffs(64, 11).addBox(-4.0F, -1.0F, -4.0F, 8.0F, 4.0F, 8.0F, new CubeDeformation(0.6F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        // smaller rounded dome on top of the shell
        PartDefinition dome = HardHat.addOrReplaceChild("dome", CubeListBuilder.create().texOffs(96, 11).addBox(-3.0F, -2.3F, -3.0F, 6.0F, 2.0F, 6.0F, new CubeDeformation(0.3F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        // reinforcement ridge running from the front to the back of the dome
        PartDefinition ridge = HardHat.addOrReplaceChild("ridge", CubeListBuilder.create().texOffs(96, 19).addBox(-1.0F, -2.8F, -4.0F, 2.0F, 1.0F, 8.0F, new CubeDeformation(0.25F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        // short brim all around the bottom edge of the shell
        PartDefinition brim = HardHat.addOrReplaceChild("brim", CubeListBuilder.create().texOffs(88, 0).addBox(-5.0F, 2.5F, -5.0F, 10.0F, 1.0F, 10.0F, new CubeDeformation(0.25F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        // front peak, slightly tilted down
        PartDefinition peak = HardHat.addOrReplaceChild("peak", CubeListBuilder.create().texOffs(64, 23).addBox(-4.0F, -0.5F, -2.0F, 8.0F, 1.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(0.0F, 2.75F, -5.0F, 0.2618F, 0.0F, 0.0F));

        PartDefinition bipedBody = partdefinition.addOrReplaceChild("body", CubeListBuilder.create().texOffs(16, 16).addBox(-4.0F, 0.0F, -2.0F, 8.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(16, 32).addBox(-4.0F, 0.0F, -2.0F, 8.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        PartDefinition toolbag = bipedBody.addOrReplaceChild("toolbag", CubeListBuilder.create(), PartPose.offset(0.0F, 0.0F, 0.0F));

        // leather tool belt around the waist (0.5 inflation: 0.25 outside the jacket layer)
        PartDefinition toolBelt = toolbag.addOrReplaceChild("toolBelt", CubeListBuilder.create().texOffs(64, 28).addBox(-4.0F, 10.0F, -2.0F, 8.0F, 2.0F, 4.0F, new CubeDeformation(0.5F)), PartPose.offset(0.0F, 0.0F, 0.0F));

        // rolled-up blueprint tucked horizontally behind the belt, in the lower back (a vertical 2x10x2 box turned on its side)
        PartDefinition blueprintRoll = toolbag.addOrReplaceChild("blueprintRoll", CubeListBuilder.create().texOffs(120, 11).addBox(-1.0F, -5.0F, -1.0F, 2.0F, 10.0F, 2.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(1.0F, 10.5F, 3.4F, 0.0F, 0.0F, 1.4708F));

        PartDefinition strapback_r1 = toolbag.addOrReplaceChild("strapback_r1", CubeListBuilder.create().texOffs(122, 46).addBox(-0.5F, -14.3F, 0.0F, 1.0F, 15.0F, 0.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-5.5665F, 9.9968F, 4.2551F, 0.0913F, 0.0015F, 0.7592F));

        PartDefinition strapfrontb_r1 = toolbag.addOrReplaceChild("strapfrontb_r1", CubeListBuilder.create().texOffs(123, 46).addBox(-0.5F, -1.8F, 0.3F, 1.0F, 5.0F, 0.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(4.4558F, -0.5558F, 1.1519F, -1.5708F, 0.0F, 0.7854F));

        PartDefinition strapfrontb_r2 = toolbag.addOrReplaceChild("strapfrontb_r2", CubeListBuilder.create().texOffs(123, 51).addBox(-0.5F, -2.5F, 0.5F, 1.0F, 6.0F, 0.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(2.6008F, 1.2992F, -3.0977F, -0.2269F, 0.0F, 0.7854F));

        PartDefinition strapfronta_r1 = toolbag.addOrReplaceChild("strapfronta_r1", CubeListBuilder.create().texOffs(126, 46).addBox(-0.5F, -8.0F, 0.0F, 1.0F, 9.0F, 0.0F, new CubeDeformation(0.0F)), PartPose.offsetAndRotation(-5.5F, 9.4F, -4.1F, -0.0873F, 0.0F, 0.7854F));

        PartDefinition bag_r1 = toolbag.addOrReplaceChild("bag_r1", CubeListBuilder.create().texOffs(106, 32).addBox(-1.9F, -3.0F, -4.0F, 3.0F, 6.0F, 8.0F, new CubeDeformation(0.03F)), PartPose.offsetAndRotation(-5.5F, 12.0F, 0.0F, 0.0F, 0.0F, 0.1222F));

        PartDefinition ruler = toolbag.addOrReplaceChild("ruler", CubeListBuilder.create(), PartPose.offset(-5.5F, 10.95F, -1.5F));

        PartDefinition ruler_r1 = ruler.addOrReplaceChild("ruler_r1", CubeListBuilder.create().texOffs(116, 54).addBox(-0.5F, -6.0F, -0.5F, 1.0F, 8.0F, 2.0F, new CubeDeformation(-0.3F)), PartPose.offsetAndRotation(0.5F, -2.0F, 3.0F, -0.2182F, 0.0F, 0.0F));

        PartDefinition ruler2 = toolbag.addOrReplaceChild("ruler2", CubeListBuilder.create(), PartPose.offset(-5.5F, 10.95F, -1.5F));

        PartDefinition ruler2_r1 = ruler2.addOrReplaceChild("ruler2_r1", CubeListBuilder.create().texOffs(110, 54).addBox(-1.1F, -4.0F, -0.7F, 1.0F, 8.0F, 2.0F, new CubeDeformation(-0.3F)), PartPose.offsetAndRotation(0.5F, -2.0F, 3.0F, -0.6531F, -0.0806F, -0.0335F));

        PartDefinition hammer = toolbag.addOrReplaceChild("hammer", CubeListBuilder.create().texOffs(118, 46).addBox(-0.5F, -4.95F, -0.5F, 1.0F, 6.0F, 1.0F, new CubeDeformation(0.0F))
          .texOffs(112, 49).addBox(-0.5F, -4.55F, -2.0F, 1.0F, 1.0F, 4.0F, new CubeDeformation(0.1F)), PartPose.offsetAndRotation(-5.5F, 10.95F, -1.5F, 0.2618F, 0.0F, 0.1309F));

        PartDefinition breast = bipedBody.addOrReplaceChild("breast", CubeListBuilder.create()
          .texOffs(64, 49).addBox(-2.65F, 1.3688F, -5.116F, 3.4F, 1.05F, 2.0F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.25F, 1.3688F, -5.116F, 3.4F, 1.05F, 2.0F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.1F, 2.3688F, -6.216F, 3.8F, 1.05F, 3.0F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.3F, 2.3688F, -6.216F, 3.8F, 1.05F, 3.0F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-3.15F, 3.3688F, -7.116F, 3.8F, 1.05F, 4.0F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.35F, 3.3688F, -7.116F, 3.8F, 1.05F, 4.0F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(-2.4F, 4.3688F, -5.916F, 3.0F, 1.05F, 5.0F, BREAST_DEFORMATION)
          .texOffs(64, 49).addBox(1.4F, 4.3688F, -5.916F, 3.0F, 1.05F, 5.0F, BREAST_DEFORMATION),
          PartPose.offsetAndRotation(-1.0F, 3.0F, 4.0F, -0.4363F, 0.0F, 0.0F));

        PartDefinition bipedRightArm = partdefinition.addOrReplaceChild("right_arm", CubeListBuilder.create().texOffs(40, 16).addBox(-2.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(40, 32).addBox(-2.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offsetAndRotation(-5.2F, 2.0F, 0.0F, 0.0F, 0.0F, 0.3491F));

        PartDefinition bipedLeftArm = partdefinition.addOrReplaceChild("left_arm", CubeListBuilder.create().texOffs(32, 48).addBox(-1.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(48, 48).addBox(-1.0F, -2.0F, -2.0F, 3.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(5.0F, 2.0F, 0.0F));

        PartDefinition bipedRightLeg = partdefinition.addOrReplaceChild("right_leg", CubeListBuilder.create().texOffs(0, 16).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(0, 32).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(-1.9F, 12.0F, 0.0F));

        PartDefinition bipedLeftLeg = partdefinition.addOrReplaceChild("left_leg", CubeListBuilder.create().texOffs(16, 48).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.0F))
          .texOffs(0, 48).addBox(-2.0F, 0.0F, -2.0F, 4.0F, 12.0F, 4.0F, new CubeDeformation(0.25F)), PartPose.offset(1.9F, 12.0F, 0.0F));

        return LayerDefinition.create(meshdefinition, 128, 64);
    }

    @Override
    public void setupAnim(@NotNull final AbstractEntityCitizen entity, float limbSwing, float limbSwingAmount, float ageInTicks, float netHeadYaw, float headPitch)
    {
        super.setupAnim(entity, limbSwing, limbSwingAmount, ageInTicks, netHeadYaw, headPitch);
        final boolean working = isWorking(entity);
        final boolean hardHatOn = working && displayHat(entity);

        body.getChild("toolbag").visible = working;
        head.getChild(HARD_HAT).visible = hardHatOn;
        // hair tied lower while the hard hat is worn, so the bun does not clip through the shell
        head.getChild(HAIR_BUN).y = hardHatOn ? HAIR_BUN_LOW_Y : HAIR_BUN_DEFAULT_Y;
    }
}
